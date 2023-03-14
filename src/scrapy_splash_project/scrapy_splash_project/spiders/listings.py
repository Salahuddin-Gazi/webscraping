import scrapy
import json
import os
from scrapy.selector import Selector


class ListingsSpider(scrapy.Spider):
    name = "listings"
    allowed_domains = ["www.centris.ca"]
    # start_urls = ["https://www.centris.ca/"]

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'

    position = {
        "startPosition": 0
    }
    query = {
        "query": {
            "UseGeographyShapes": 0,
            "Filters": [],
            "FieldsValues": [
                {
                    "fieldId": "Category",
                    "value": "Residential",
                    "fieldConditionId": "",
                    "valueConditionId": ""
                },
                {
                    "fieldId": "SellingType",
                    "value": "Rent",
                    "fieldConditionId": "",
                    "valueConditionId": ""
                },
                {
                    "fieldId": "LandArea",
                    "value": "SquareFeet",
                    "fieldConditionId": "IsLandArea",
                    "valueConditionId": ""
                },
                {
                    "fieldId": "RentPrice",
                    "value": 0,
                    "fieldConditionId": "ForRent",
                    "valueConditionId": ""
                },
                {
                    "fieldId": "RentPrice",
                    "value": 1500,
                    "fieldConditionId": "ForRent",
                    "valueConditionId": ""
                }
            ]
        },
        "isHomePage": True
    }
    page = 1

    def start_requests(self):

        # print(json.dumps(query))
        yield scrapy.Request(
            url="https://www.centris.ca/property/UpdateQuery",
            method="POST",
            body=json.dumps(self.query),
            headers={
                'Content-Type': 'application/json',
                'user-agent': self.user_agent
            },
            callback=self.update_query,
        )

    def update_query(self, response):
        yield scrapy.Request(
            url="https://www.centris.ca/Property/GetInscriptions",
            method="POST",
            body=json.dumps(self.position),
            headers={
                'Content-Type': 'application/json',
                'user-agent': self.user_agent
            },
            callback=self.parse,
        )

    def parse(self, response):
        resp_dict = json.loads(response.body)
        # print('<-------------->')

        # print(resp_dict["d"]["Result"]["html"])
        # print(resp_dict.get("d").get("Result").get("html"))

        html = resp_dict.get("d").get("Result").get("html")
        count = resp_dict.get("d").get("Result").get("count")
        inc_number = resp_dict.get("d").get("Result").get("inscNumberPerPage")

        # file = os.getcwd()+'\\scrapy_splash_project\\spiders\\output\\index.html'
        # with open(file, 'w') as f:
        #     f.write(html)

        sel = Selector(text=html)
        listings = sel.xpath(
            "//div[contains(@class, \"property-thumbnail-item\")]")

        for listing in listings:
            description = listing.xpath('.//div[@class="description"]')
            location = description.xpath('.//div[@class="location-container"]')

            category = location.xpath(
                './span[@class="category"]/div/text()').get().strip()
            # address = ' '.join(location.xpath(
            #     './span[@class="address"]/div/text()').getall())
            # city = ' '.join(location.xpath(
            #     './span[@class="address"]/div[2]/text()').get())
            city = location.xpath(
                './span[@class="address"]/div[2]/text()').get()
            price = description.xpath(
                './/div[@class="price"]/meta[@itemprop="price"]/@content').get()
            url = listing.xpath(
                './/a[@class="property-thumbnail-summary-link"]/@href').get()

            yield {
                'page': self.page,
                'category': category,
                'city': city,
                'price': price,
                'url': url
            }
        self.page += 1
        if self.position["startPosition"] <= count:
            self.position["startPosition"] += inc_number
            # print('<---------------->')
            # print(self.position["startPosition"])
            yield scrapy.Request(
                url="https://www.centris.ca/Property/GetInscriptions",
                method="POST",
                body=json.dumps(self.position),
                headers={
                    'Content-Type': 'application/json',
                    'user-agent': self.user_agent
                },
                callback=self.parse,
            )
