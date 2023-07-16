# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.selector import Selector

from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags
import json
import re


class SteamTopSellingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    def remove_minus(value):
        return value.replace('-', '').strip()

    def handle_platform(list_platforms):

        # I know it's weird but this the way 🤣🤣
        # itemloader directly work with the list not like it gives a list to work with,
        # best of luck to myself

        item = list_platforms.split(' ')[-1]
        match item:
            case 'win':
                # platforms.append('Windows')
                return 'Windows'
            case 'mac':
                # platforms.append('Mac')
                return 'Mac'
            case 'linux':
                # platforms.append('Linux')
                return 'Linux'
            case 'vr_supported':
                # platforms.append('VR Supported')
                return 'VR Support'
            case default:
                # pass
                return

    def handle_reviews(review_text):
        match = re.search(r"^(\D*)", review_text)
        if match:
            return match.group()

    def handle_price(value):
        selector_obj = Selector(text=value, type='html')
        original_price = ''
        if len(selector_obj.xpath('.//span/strike')) > 0:
            original_price = selector_obj.xpath(
                './/span/strike/text()').get().replace('$', '').strip()
            return original_price

        original_price = selector_obj.xpath(
            './/text()').get().replace('$', '').strip()

        return original_price

    index = scrapy.Field(
        output_processor=TakeFirst()
    )

    name = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    link = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    image_url = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    release_date = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    platforms = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_platform),
        # output_processor=json.dumps
    )
    reviews = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_reviews),
        output_processor=TakeFirst()
    )
    reviews_original = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    original_price = scrapy.Field(
        input_processor=MapCompose(handle_price),
        output_processor=TakeFirst()
    )
    discount = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_minus),
        output_processor=TakeFirst()
    )
