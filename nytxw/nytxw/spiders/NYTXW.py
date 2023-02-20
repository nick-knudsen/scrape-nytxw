import scrapy
import toml

def get_secrets():
    secret_path = 'secrets.toml'
    secrets = toml.load(secret_path)
    username = secrets['NYTXW']['username']
    password = secrets['NYTXW']['password']

    return username, password

def authentication_failed(response):
    pass

class NytxwSpider(scrapy.Spider):
    name = "NYTXW"
    allowed_domains = ["nytimes.com"]
    start_urls = ["https://www.nytimes.com/crosswords/game/daily/1993/11/21"]

    def parse(self, response):
        username, password = get_secrets()
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': username, 'password': password},
            callback=self.after_login
        )
        pass
