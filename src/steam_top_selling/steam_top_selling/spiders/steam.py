import scrapy
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

from scrapy_splash import SplashRequest

from .utils import URL, USER_AGENT
from ..items import SteamTopSellingItem


class SteamSpider(scrapy.Spider):
    name = "steam"
    allowed_domains = ["store.steampowered.com"]
    # start_urls = ["https://store.steampowered.com/"]
    custom_settings = {"CLOSESPIDER_ITEMCOUNT": 500}

    item_count = 0

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))

            local num_scrolls = 10
            local scroll_delay = 2.0

            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc("function(){return document.body.scrollHeight;}")

            local scrollHeight = 0
            for _=1, num_scrolls do
                local currentHeight = get_body_height()
                scroll_to(scrollHeight, currentHeight)
                scrollHeight = scrollHeight + currentHeight
                splash:wait(scroll_delay)
            end

            return splash:html()
        end
    '''

    # script = '''
    # function main(splash, args)
    #     assert(splash:go(args.url))
    #     assert(splash:wait(0.5))
    #     local callbackfn = splash:evaljs("()=>{let l=0,o,$=0;clearInterval(o),o=setInterval(()=>{console.log(l),l++,console.log($),window.scrollTo(0,document.body.scrollHeight),$+=document.body.scrollHeight,l>=10&&clearInterval(o)},2e3)}")
    #     callbackfn()
    #     return splash:html()
    # end
    # '''

    def handling_item_count(self):
        # line 16, dumb 👍 custom_settings = {"CLOSESPIDER_ITEMCOUNT": 40}
        if (self.settings['CLOSESPIDER_ITEMCOUNT'] and int(self.settings['CLOSESPIDER_ITEMCOUNT']) == self.item_count):
            raise CloseSpider('CLOSESPIDER_ITEMCOUNT limit reached - ' +
                              str(self.settings['CLOSESPIDER_ITEMCOUNT']))
        else:
            self.item_count += 1

    def start_requests(self):
        yield SplashRequest(
            url=URL,
            # endpoint="execute",
            headers={'user-agent': USER_AGENT},
            # args={
            #     'lua_source': self.script,
            # },
            callback=self.parse
        )

    def parse(self, response):

        # print('<================>')
        # print(self.settings['CLOSESPIDER_ITEMCOUNT'])

        res_games = Selector(response=response, type='html')
        games = res_games.xpath('//div[@id="search_resultsRows"]/a')

        for game in games:

            l = ItemLoader(
                item=SteamTopSellingItem(), selector=game, response=response)

            l.add_value("index", self.item_count)

            l.add_xpath(
                "name", './/div[contains(@class, "col search_name")]/span/text()')

            l.add_xpath('link', './@href')

            l.add_xpath(
                "image_url", './div[@class="col search_capsule"]/img/@src')

            l.add_xpath(
                "release_date", './/div[contains(@class, "search_released")]/text()')

            l.add_xpath(
                "platforms", './/div/span[contains(@class, \'platform_img\') or @class="vr_supported"]/@class')

            l.add_xpath(
                "reviews", './/div[contains(@class, "search_reviewscore")]/span[contains(@class, "positive") or contains(@class, "negative") or contains(@class, "mixed")]/@data-tooltip-html')

            l.add_xpath(
                "reviews_original", './/div[contains(@class, "search_reviewscore")]/span[contains(@class, "positive") or contains(@class, "negative") or contains(@class, "mixed")]/@data-tooltip-html')

            l.add_xpath(
                'original_price', './/div[contains(@class, "search_price")]/div[contains(@class, "search_price") or contains(@class, "search_price discounted")]')

            l.add_xpath(
                'discount', './/div[contains(@class, "search_discount")]/span/text()')

            self.handling_item_count()

            yield l.load_item()
