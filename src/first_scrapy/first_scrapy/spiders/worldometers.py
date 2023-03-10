import scrapy


class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info"]
    start_urls = [
        "https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        # title = response.xpath('//h1/text()').get()
        xpath_countries = '//td/a/'
        countries = response.xpath(f'{xpath_countries}text()').getall()
        links = response.xpath(f'{xpath_countries}@href').getall()

        # Concat way
        # domain = "https://www.worldometers.info/"
        # for i in range(len(links)):
        #     links[i] = domain+links[i]
        #     yield scrapy.Request(url=links[i])

        for i in range(len(links)):

            # Absolute way
            # absolute_url = response.urljoin(link)
            # yield scrapy.Request(url=absolute_url)

            # Relative way
            yield response.follow(url=links[i], callback=self.parse_country, meta={'country': countries[i]})

    def parse_country(self, response):
        rows = response.xpath(
            "(//table[contains(@class, \"table\")])[1]/tbody/tr")
        # years = []
        # populations = []
        country = response.request.meta['country']
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td/strong/text()").get()
            # years.append(year)
            # populations.append(population)

            yield {
                'country': country,
                'year': year,
                'population': population
            }
        # yield {
        #     'year': years,
        #     'population': populations
        # }
