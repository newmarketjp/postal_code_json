# Copyright 2023 Newmarket Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import logging
import numpy as np
import pandas as pd
import scrapy
import json
import os
import zipfile
from scrape_postal_code.items import PostalCodesItem
import re

class PostalCodeSpider(scrapy.Spider):
    name = "postal_code_spider"
    allowed_domains = ["japanpost.jp"]
    start_urls = ["https://www.post.japanpost.jp/zipcode/dl/utf-zip.html"]
    dist_path = "../dist"

    ztoh = str.maketrans('０１２３４５６７８９', '0123456789')
    htoz = str.maketrans('0123456789', '０１２３４５６７８９')
    extract_brackets = re.compile("(^[^、〜\−]+)（(.+?)）$")
    extract_kakko = re.compile("([^、]+)(「.+?」)")
    extract_kakko2 = re.compile("(「|＜).+?(」|＞)")
    extract_suffix_label = re.compile("([\d、〜\−]+)(丁目|線|条|番地|地割|チョウメ|セン|ジョウ|バンチ|チワリ)$")
    need_extract = re.compile("^[\d、〜\−]+(丁目|チョウメ)$")
    extract_range = re.compile("\w*?(\d+)\w*?[〜\−](\w*?)(\d+)、?.*$")
    normalize_brackets1_1 = re.compile("^(.+?[^（〜\−])((?:第|ダイ).+)$")
    normalize_brackets1_2 = re.compile("（.+?）$")
    normalize_brackets2_1 = re.compile("^([^（）\d]+)(第|ダイ)?(\d+(?:地割|チワリ))([〜\−])([^（）\d]+)(第|ダイ)?(\d+(?:地割|チワリ))$")

    def extract_oaza(self, row):
        try:
            return self._extract_chome(row["oaza"])
        except Exception as e:
            print("Caught error at line: " + row)
            raise e

    def extract_oaza_kana(self, row):
        try:
            return self._extract_chome(row["oaza_kana"])
        except Exception as e:
            print("Caught error at line: " + row)
            raise e

    def _extract_chome(self, line):
        chome_list = []
        base_line = line.translate(PostalCodeSpider.ztoh)

        matched_normalize_brackets1_1 = re.match(PostalCodeSpider.normalize_brackets1_1, base_line)
        if matched_normalize_brackets1_1 is not None and not base_line.startswith("シュンコウダイ"):
            suffix_brackets = re.sub(PostalCodeSpider.normalize_brackets1_2, "", matched_normalize_brackets1_1.group(2))
            if suffix_brackets is not None:
                base_line = matched_normalize_brackets1_1.group(1) + "（" + suffix_brackets + "）"
            else:
                base_line = matched_normalize_brackets1_1.group(1)

        matched_normalize_brackets2_1 = re.match(PostalCodeSpider.normalize_brackets2_1, base_line)
        if matched_normalize_brackets2_1 is not None and matched_normalize_brackets2_1.group(1) == matched_normalize_brackets2_1.group(4):
            base_line = "{}（{}{}〜{}{}）".format(matched_normalize_brackets2_1.group(1),
                                               matched_normalize_brackets2_1.group(2) or "",
                                               matched_normalize_brackets2_1.group(3),
                                               matched_normalize_brackets2_1.group(5) or "",
                                               matched_normalize_brackets2_1.group(6))

        town = None
        matched_extract_brackets = re.match(PostalCodeSpider.extract_brackets, base_line)
        if matched_extract_brackets is not None:
            town = matched_extract_brackets.group(1)
            base_line = matched_extract_brackets.group(2)

            base_line = re.sub(PostalCodeSpider.extract_kakko2, "", base_line)

            matched_need_extract = re.match(PostalCodeSpider.need_extract, base_line)

            suffix_label = None
            prefix_label = None

            matched_extract_suffix_label = re.match(PostalCodeSpider.extract_suffix_label, base_line)
            if matched_extract_suffix_label is not None:
                base_line = matched_extract_suffix_label.group(1)
                suffix_label = matched_extract_suffix_label.group(2)

            for range_cell in base_line.split("、"):
                if matched_need_extract is not None:

                    matched_extract_suffix_label = re.match(PostalCodeSpider.extract_suffix_label, range_cell)
                    if matched_extract_suffix_label is not None:
                        range_cell = matched_extract_suffix_label.group(1)
                        suffix_label = matched_extract_suffix_label.group(2)

                    matched_extract_range = re.match(PostalCodeSpider.extract_range, range_cell)
                    if matched_extract_range is not None:
                        start_idx = int(matched_extract_range.group(1))
                        prefix = matched_extract_range.group(2)
                        end_idx = int(matched_extract_range.group(3))
                        for i in range(start_idx, end_idx + 1):
                            if suffix_label is not None:
                                chome_list.append("{}{}{}".format(prefix, str(i), suffix_label))
                            elif prefix_label is not None:
                                chome_list.append("{}{}".format(prefix_label, str(i)))
                            else:
                                chome_list.append(str(i))
                    else:
                        try:
                            int(range_cell)  # try cast to integer
                            if suffix_label is not None:
                                chome_list.append("{}{}".format(range_cell, suffix_label))
                            elif prefix_label is not None:
                                chome_list.append("{}{}".format(prefix_label, range_cell))
                        except ValueError as e:
                            chome_list.append(range_cell)
                else:
                    try:
                        int(range_cell)  # try cast to integer
                        if suffix_label is not None:
                            chome_list.append("{}{}".format(range_cell, suffix_label))
                        elif prefix_label is not None:
                            chome_list.append("{}{}".format(prefix_label, range_cell))
                        else:
                            chome_list.append(str(range_cell))
                    except ValueError as e:
                        if suffix_label is not None and ( "〜" in range_cell or "−" in range_cell ):
                            chome_list.append("{}{}".format(range_cell, suffix_label))
                        else:
                            chome_list.append(range_cell)
            chome_list = [x.translate(PostalCodeSpider.htoz) for x in chome_list]
        else:
            town = base_line
            chome_list = None
        town = town.translate(PostalCodeSpider.htoz)
        return (town, chome_list)

    def cleansing_dataframe(self, df):
        """
        CSV形式のデータを綺麗にする

        https://qiita.com/yuki-watanabe/items/b10eb83a915c25c20060

        :param df:
        :return: クレンジング済みのdf
        """
        df.columns = ["x0401", "old_postal_code", "postal_code", "prefecture_kana", "city_kana",
                      "oaza_kana", "prefecture", "city", "oaza", "split_oaza", "must_koaza", "has_chome", "multiple_oaza", "update_status", "update_reason"]

        # 数値フィールドは数値に変換しておく。
        for k in ["x0401", "old_postal_code", "postal_code", "prefecture_kana", "city_kana", "oaza_kana", "prefecture", "city", "oaza"]:
            df[k] = df[k].astype(str)
        for k in ["update_status", "update_reason"]:
            df[k] = df[k].astype(int)
        for k in ["split_oaza", "must_koaza", "has_chome", "multiple_oaza"]:
            df[k] = df[k].astype(bool)

        df["x0401"] = df["x0401"].str.zfill(5)
        df["old_postal_code"] = df["old_postal_code"].str.zfill(5)
        df["postal_code"] = df["postal_code"].str.zfill(7)
        df["oaza_original"] = df["oaza"]

        df["oaza_kana"] = df["oaza_kana"].str.replace("イカニケイサイガナイバアイ", "")
        df["oaza"] = df["oaza"].str.replace("以下に掲載がない場合", "")

        df["oaza"] = df["oaza"].str.replace("琴平町の次に１〜４２６番地がくる場合（川東）", "１〜４２６番地（川東）")
        df["oaza"] = df["oaza"].str.replace("琴平町の次に４２７番地以降がくる場合（川西）", "４２７番地以降（川西）")


        df["oaza"] = df["oaza"].replace("（次のビルを除く）$", "", regex=True)
        df["oaza"] = df["oaza"].replace({r'(.+)(第.*?地割〜第.*?地割)（.*?）$':r'\1（\2）'}, regex=True)

        # 大字にある削除する要素をmemoの形式として残す(表示用)
        df["oaza_annotation"] = None
        oaza_with_anotations = df.loc[:, ["oaza"]].apply(lambda x: self.extract_oaza(x), axis=1)
        df.loc[:, ["oaza", "oaza_annotation"]] = np.asarray([[t[0], t[1]] for t in oaza_with_anotations], dtype="object")

        oaza_kana_with_anotations = df.loc[:, ["oaza_kana"]].apply(lambda x: self.extract_oaza_kana(x), axis=1)
        df.loc[:, ["oaza_kana"]] = np.asarray([[t[0]] for t in oaza_kana_with_anotations], dtype="object")

        ## 下記はそのまま表記に利用する
#        df["oaza"] = df["oaza"].replace(".+（[０-９]+階）$", "", regex=True)
#        df["oaza"] = df["oaza"].replace(".+（地階・階層不明）$", "", regex=True)
#        df["oaza"] = df["oaza"].replace(".+（その他）$", "", regex=True)
#        df.loc[df["has_chome"], ["oaza", "oaza_kana"]] = df.loc[df["has_chome"], ["oaza", "oaza_kana"]].replace("（.*）$", "", regex=True)
#        df.loc[df["split_oaza"], ["oaza", "oaza_kana"]] = df.loc[df["split_oaza"], ["oaza", "oaza_kana"]].replace("（.*）$", "", regex=True)

        return df

    def write_json(self, file_name, obj):
        dist_path = PostalCodeSpider.dist_path
        if not os.path.exists(dist_path):
            os.mkdir(dist_path)
        with open("{}/{}".format(dist_path, file_name), "w") as f:
            json.dump(obj, f, indent=True, ensure_ascii=False)

    def write_csv(self, file_name, df):
        dist_path = PostalCodeSpider.dist_path
        if not os.path.exists(dist_path):
            os.mkdir(dist_path)
        df.to_csv("{}/{}".format(dist_path, file_name))

    def parse(self, response):
        """
        スクレイピングのデータ処理を行う。

        :param response:
        :return:
        """
        # 青果標準商品コードのURLリンクを探索する
        next_page_url = None
        for sel in response.xpath('//*[@id="main-box"]/div/div/ul[1]/li/a'):
            next_page_url = response.urljoin(sel.xpath("@href").get())
            break
        self.log("郵便番号のCSVファイルへのリンク： " + next_page_url, logging.INFO)

        if next_page_url is None:
            raise Exception("郵便番号のCSVファイルへのリンクが見つかりませんでした。")
        return scrapy.Request(next_page_url, callback=self.parse_zip)

    def parse_zip(self, response):
        zip = zipfile.ZipFile(io.BytesIO(response.body))

        # CSVファイルをPandasで読み込む
        df = pd.read_csv(zip.open("utf_all.csv"), header=None)

        # 加工しやすいようにデータをクレンジングする
        df = self.cleansing_dataframe(df)

        # データフレームからデータの形式に変換する
        postal_codes = self.parse_items(df)

        item = PostalCodesItem()
        item["postal_codes"] = postal_codes

        yield item


    def parse_items(self, df):
        """
        PandasのDataFrameの形式から中間データへ変換する

        :param df:
        :return: list形式
        """
        postal_codes = []
        for i, r in df.iterrows():
            postal_codes.append(r.to_dict())

        return postal_codes

    def generate_map(self, postal_codes):
        """
        postal_codesのリストをpostal_code : [
            record,
            record,
        ]

        :param postal_codes:
        :return: postal_codeをキーにしたマップ
        """

        postal_code_map = {}
        for v in postal_codes:
            key1 = v["postal_code"]

            if not key1 in postal_code_map.keys():
                postal_code_map[key1] = [v]
            else:
                postal_code_map[key1].append(v)

        return postal_code_map
