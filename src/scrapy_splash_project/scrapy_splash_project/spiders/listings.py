import scrapy
import json
import os
from scrapy.selector import Selector
from scrapy_splash import SplashRequest


class ListingsSpider(scrapy.Spider):
    name = "listings"

    http_user = 'user'
    http_pass = 'userpass'

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
                    "value": 500,
                    "fieldConditionId": "ForRent",
                    "valueConditionId": ""
                }
            ]
        },
        "isHomePage": True
    }

    script = '''
    function main(splash, args)
        splash:on_request(
            function(request) 
                if request.url:find('css') then request.abort()
                end
            end
        )
        splash.images_enabled = false
        splash.js_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(0.5))
        return splash:html()
    end
    '''

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

            abs_url = "https://www.centris.ca"+url
            print('<------------------->')
            print(abs_url)
            # yield {
            #     'category': category,
            #     'city': city,
            #     'price': price,
            #     'url': abs_url
            # }

            yield SplashRequest(
                url=abs_url,
                endpoint="execute",
                callback=self.parse_summary,
                args={
                    'lua_source': self.script
                },
                meta={
                    'cat': category,
                    'pri': price,
                    'city': city,
                    'url': abs_url
                }
            )

        if self.position["startPosition"] <= count:
            self.position["startPosition"] += inc_number
            # print('<---------------->')
            # print(self.position["startPosition"])
            print('<------------------->')
            print(self.position["startPosition"])
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

    def parse_summary(self, response):
        # address = ' '.join(response.xpath(
        #     '//h2[@itemprop="address"]/font/font/text()').getall())
        xpath_fn = response.xpath
        address = xpath_fn(
            '//h2[@itemprop="address"]//text()').get()

        # desc = xpath_fn(
        #     '//div[@itemprop="description"]//text()')

        # description = desc.get().strip() if desc else ''

        description = xpath_fn(
            'normalize-space(//div[@itemprop="description"]//text())').get()
        # features_list = xpath_fn(
        #     '//div[contains(@class, "description")]//div[contains(@class, "teaser")]//font/font').getall()[3:]
        # features = ' '.join(features_list)
        features = xpath_fn(
            '//div[contains(@class, "teaser")]//span[@class="match-score-text"]//text()').get()

        metaData = response.request.meta
        category = metaData['cat']
        price = metaData['pri']
        city = metaData['city']
        url = metaData['url']

        yield {
            'address': address,
            'category': category,
            'description': description,
            'features': features,
            'city': city,
            'price': price,
            'url': url
        }
