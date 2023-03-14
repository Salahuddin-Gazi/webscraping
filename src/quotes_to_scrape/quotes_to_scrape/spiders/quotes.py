import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/api/quotes?page=1"]

    def parse(self, response):
        json_response = json.loads(response.body)
        quotes = json_response['quotes']

        for quote in quotes:
            yield {
                'page': json_response['page'],
                'author': quote['author']['name'],
                'tags': quote['tags'],
                'quotes': quote['text'],
            }

        has_next = json_response['has_next']
        if has_next:
            next_page_number = json_response['page'] + 1
            url = f"https://quotes.toscrape.com/api/quotes?page={next_page_number}"
            yield scrapy.Request(url, callback=self.parse)
