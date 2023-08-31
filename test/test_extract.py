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


def test__extract_chome1():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('西十九条南（３５〜３８、４１、４２丁目）')
    assert result[0] == "３５丁目"
    assert result[1] == "３６丁目"
    assert result[2] == "３７丁目"
    assert result[3] == "３８丁目"
    assert result[4] == "４１丁目"
    assert result[5] == "４２丁目"

def test__extract_chome2():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('西美里別（１１３〜７９１番地、西活込、西上、西中）')
    assert result[0] == "１１３〜７９１番地"
    assert result[1] == "西活込"
    assert result[2] == "西上"
    assert result[3] == "西中"

def test__extract_chome3():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('折茂（今熊「２１３〜２３４、２４０、２４７、２６２、２６６、２７５、２７７、２８０、２９５、１１９９、１２０６、１５０４を除く」、大原、沖山、上折茂「１−１３、７１−１９２を除く」）')
    assert result[0] == "今熊"
    assert result[3] == "上折茂"

def test__extract_chome4():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('犬落瀬（内金矢、内山、岡沼、金沢、金矢、上淋代、木越、権現沢、四木、七百、下久保「１７４を除く」、下淋代、高森、通目木、坪毛沢「２５、６３７、６４１、６４３、６４７を除く」、中屋敷、沼久保、根古橋、堀切沢、南平、柳沢、大曲）')
    assert result[0] == "内金矢"
    assert result[1] == "内山"
    assert result[10] == "下久保"
    assert result[14] == "坪毛沢"

def test__extract_chome5():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('犬落瀬（内金矢、内山、岡沼、金沢、金矢、上淋代、木越、権現沢、四木、七百、下久保「１７４を除く」、下淋代、高森、通目木、坪毛沢「２５、６３７、６４１、６４３、６４７を除く」、中屋敷、沼久保、根古橋、堀切沢、南平、柳沢、大曲）')
    assert result[0] == "内金矢"
    assert result[1] == "内山"
    assert result[10] == "下久保"
    assert result[14] == "坪毛沢"

def test__extract_chome6():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('越中畑６４地割〜越中畑６６地割')
    assert town == "越中畑"
    assert result[0] == "６４地割〜６６地割"

def test__extract_chome7():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('十日町（猫屋敷３２９〜３５６）')
    assert result[0] == "猫屋敷３２９〜３５６"

def test__extract_chome8():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('藤原（１０４７〜１２６８及び下平）')
    assert result[0] == "１０４７〜１２６８及び下平"

def test__extract_chome9():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('藤原（その他）')
    assert result[0] == "その他"

def test__extract_chome10():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('名駅（１−１−８、１−１−１２、１−１−１３、１−１−１４、１−３−４、１−３−７）')
    assert result[0] == "１−１−８"
    assert result[1] == "１−１−１２"
    assert result[2] == "１−１−１３"
    assert result[3] == "１−１−１４"
    assert result[4] == "１−３−４"
    assert result[5] == "１−３−７"

def test__extract_chome11():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('音別町音別原野基線（二俣）')
    assert result[0] == "二俣"

def test__extract_chome12():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('種市第３９地割〜第４５地割（角浜、伝吉）')
    assert result[0] == "第３９地割〜第４５地割"

def test__extract_chome13():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('中嶋（１−９７〜１１６）')
    assert result[0] == "１−９７〜１１６"  # カナでは1-97-116なのでタイポ？

def test__extract_chome14():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('箱石（第２地割「７０〜１３６」〜第４地割「３〜１１」）')
    assert result[0] == "第２地割〜第４地割"

def test__extract_chome15():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('川井（第９地割〜第１１地割）')
    assert result[0] == "第９地割〜第１１地割"

def test__extract_chome16():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('北工業団地（３、５番地）')
    assert result[0] == "３番地"
    assert result[1] == "５番地"

def test__extract_chome17():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('中央ＳＳ３０住友生命仙台中央ビル（１２階）')
    assert result[0] == "１２階"

def test__extract_chome18():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('五橋（３丁目）')
    assert result[0] == "３丁目"

def test__extract_chome19():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('山田（山田山２４−２）')
    assert result[0] == "山田山２４−２"

def test__extract_chome20():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('唐桑町西舞根（２００番以上）')
    assert result[0] == "２００番以上"

def test__extract_chome21():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('円田（釜沢、善舞森、土浮谷地、土浮山２〜５番地）')
    assert result[0] == "釜沢"
    assert result[1] == "善舞森"
    assert result[2] == "土浮谷地"
    assert result[3] == "土浮山２〜５番地"

def test__extract_chome22():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('大山（丁目）')
    assert result[0] == "丁目"

def test__extract_chome23():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('添川（渡戸沢「筍沢温泉」）')
    assert result[0] == "渡戸沢"

def test__extract_chome24():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('上寺島（１６５３、１６６１、１６７８、１６９４番地）')
    assert result[0] == "１６５３番地"
    assert result[1] == "１６６１番地"
    assert result[2] == "１６７８番地"
    assert result[3] == "１６９４番地"

def test__extract_chome25():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('宇奈月町音澤（１０００〜）')
    assert result[0] == "１０００〜"

def test__extract_chome26():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('宇奈月町音澤（１〜９９９）')
    assert result[0] == "１〜９９９"

def test__extract_chome27():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('南郷通（南）')
    assert result[0] == "南"

def test__extract_chome28():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('常盤（その他）')
    assert result[0] == "その他"

def test__extract_chome29():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('抜海村（上勇知、下勇知、夕来、オネトマナイ）')
    assert result[0] == "上勇知"
    assert result[1] == "下勇知"
    assert result[2] == "夕来"
    assert result[3] == "オネトマナイ"

def test__extract_chome30():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('常盤（１〜１３１番地）')
    assert result[0] == "１〜１３１番地"

def test__extract_chome31():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('藤野（４００、４００−２番地）')
    assert result[0] == "４００番地"
    assert result[1] == "４００−２番地"

def test__extract_chome32():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('留萌原野（１〜１２線）')
    assert result[0] == "１〜１２線"

def test__extract_chome33():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('安川（３）')
    assert result[0] == "３"

def test__extract_chome34():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('上野々３９地割')
    assert town == "上野々３９地割"

def test__extract_chome35():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('中村５８地割、中村５９地割')
    assert town == "中村５８地割、中村５９地割"


def test__extract_chome_kana1():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('ハコイシ（ダイ２チワリ＜７０−１３６＞−ダイ４チワリ＜３−１１＞）')
    assert result[0] == "ダイ２チワリ−ダイ４チワリ"

def test__extract_chome_kana2():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('シュンコウダイ１ジョウ')
    assert town == "シュンコウダイ１ジョウ"

def test__extract_chome_kana3():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('ウエノノ３９チワリ')
    assert town == "ウエノノ３９チワリ"

def test__extract_chome_kana4():
    spider = PostalCodeSpider()
    town, result = spider._extract_chome('ナカムラ５８チワリ、ナカムラ５９チワリ')
    assert town == "ナカムラ５８チワリ、ナカムラ５９チワリ"
