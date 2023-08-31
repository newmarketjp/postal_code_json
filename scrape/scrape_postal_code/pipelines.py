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

from itemadapter import ItemAdapter
import scrapy
from scrape_postal_code.spiders.postal_code_spider import PostalCodeSpider


class PostalCodesWriterPipeline:
    def process_item(self, item, spider):
        postal_codes = item["postal_codes"]
        # 郵便番号をJSON形式で出力する
        spider.write_json("postal_codes.json", postal_codes)

        return item

class PostalCodesMapWriterPipeline:
    def process_item(self, item, spider: PostalCodeSpider):
        postal_codes = item["postal_codes"]

        generated = spider.generate_map(postal_codes)
        # 郵便番号をJSON形式で出力する
        spider.write_json("postal_code_map.json", generated)

        return item