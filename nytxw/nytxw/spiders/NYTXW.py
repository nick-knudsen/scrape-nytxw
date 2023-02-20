import scrapy

def authentication_failed(response):
    pass

class NytxwSpider(scrapy.Spider):
    name = "NYTXW"
    allowed_domains = ["nytimes.com"]
    start_urls = ["https://www.nytimes.com/crosswords/game/daily/1993/11/21"]

    def parse(self, response):
        pass
