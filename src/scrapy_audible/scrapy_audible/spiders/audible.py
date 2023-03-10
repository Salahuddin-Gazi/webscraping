import scrapy

page_index = 1


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"]
    # start_urls = ["https://www.audible.com/search/"]

    def start_requests(self):
        yield scrapy.Request(url="https://www.audible.com/search/", callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'})

    def parse(self, response):
        product_list_items = response.xpath(
            '//div[@class="adbl-impression-container "]//li[contains(@class, "productListItem")]')

        global page_index
        for product in product_list_items:
            book_title = product.xpath(
                './/h3[contains(@class, "bc-heading")]/a/text()').get()
            # authors may be multiple
            book_author = product.xpath(
                './/li[contains(@class, "authorLabel")]/span/a/text()').getall()
            book_length = product.xpath(
                './/li[contains(@class, "runtimeLabel")]/span/text()').get()
            yield {
                'page': page_index,
                'title': book_title,
                'author': book_author,
                'length': book_length,
                'Agent': response.request.headers['User-Agent'],
            }
            print("<-------------->\n")

        page_index += 1
        pagination = response.xpath(
            '//ul[contains(@class, "pagingElements")]')
        next_page_url = pagination.xpath(
            './/span[contains(@class, "nextButton")]/a/@href').get()
        print("<-------------->\n")
        print(next_page_url)
        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'})
