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


import pytest
import pandas as pd
from scrape_postal_code.spiders.postal_code_spider import PostalCodeSpider


def test_cleansing_dataframe1():
    df = pd.read_csv("./test_parse/utf_all.csv", header=None)
    spider = PostalCodeSpider()
    PostalCodeSpider.dist_path = "./test_parse/dist"
    df = spider.cleansing_dataframe(df)
    spider.write_csv("postal_codes.csv", df)


def test_parse_item1():
    df = pd.read_csv("./test_parse/utf_all.csv", header=None)
    spider = PostalCodeSpider()
    PostalCodeSpider.dist_path = "./test_parse/dist"
    df = spider.cleansing_dataframe(df)
    items = spider.parse_items(df)
    spider.write_json("postal_codes.json", items)

    print("count: {}".format(len(items)))

def test_parse_map1():
    df = pd.read_csv("./test_parse/utf_all.csv", header=None)
    spider = PostalCodeSpider()
    PostalCodeSpider.dist_path = "./test_parse/dist"
    df = spider.cleansing_dataframe(df)
    items = spider.parse_items(df)

    postal_codes_map = spider.generate_map(items)
    spider.write_json("postal_code_map.json", postal_codes_map)
