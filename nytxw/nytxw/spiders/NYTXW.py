import scrapy
import toml
import json

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
 
    def start_requests(self):
        urls = ["https://www.nytimes.com/crosswords/game/daily/1993/11/21"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.login)

    def login(self, response):
        login_page = response.css('div.pz-nav__actions a::attr(href)').extract()[1] 
        login_page = response.urljoin(login_page)
        yield scrapy.Request(login_page, callback=self.enter_email)

    def enter_email(self, response):
        email, password = get_secrets()
        enter_password = scrapy.FormRequest.from_response(
            response,
            formdata={'email': email},
            callback=self.enter_password
        )
    
    def enter_password(self, response):
        email, password = get_secrets()
        return scrapy.FormRequest.from_response(
            response,
            formdata={'email': email,
                      'password': password},
                      callback=self.parse
        )

    def parse(self, response):
        request = scrapy.Request.from_curl(
             'curl "https://www.nytimes.com/svc/crosswords/v6/puzzle/daily/1993-11-21.json" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0" -H "Accept: */*" -H "Accept-Language: en-US,en;q=0.5" -H "Accept-Encoding: gzip, deflate, br" -H "nyt-s: 28WClUEqbYsk/2tc0CytxdtTUkmpkAZ3yhyN4PPGbjvtm1dbGWcyksd8/Mayx8zYDEjOoea6bgYnR0Iuax90AMVX4OP9myeO3UVXc.uxH6.2LHskgEdkx/Q0DKctcwi2P5IZMElomWjXBvnmPVCuTVr1PoORlAuucOQP8rCo4ZfvOTREDRO.unS000^^^^^^^^CBQSKQiSqM-fBhCKqc-fBhoSMS3OXZvQh7GOX6h5xk2FAP3AIMXSpC4qAh4DGkDUwDcMbERvxKZCQBQFV5MFWXOc-TbclbguditbAxeT2cn6X6LZFynoQyFdsWOS2l7LGgh46JTxKQBrAMdQBHYM" -H "Content-type: application/x-www-form-urlencoded" -H "DNT: 1" -H "Connection: keep-alive" -H "Referer: https://www.nytimes.com/crosswords/game/daily/1993/11/21?login=email&auth=login-email" -H "Cookie: nyt-a=lMjWZaRnxmJF81gXE8abJL; nyt-gdpr=0; nyt-purr=cfhhpfhhhckfhd; edu_cig_opt=^%^7B^%^22isEduUser^%^22^%^3Afalse^%^7D; nyt-jkidd=uid=0&lastRequest=1676916441888&activeDays=^%^5B0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C1^%^5D&adv=1&a7dv=1&a14dv=1&a21dv=1&lastKnownType=anon&newsStartDate=&entitlements=; b2b_cig_opt=^%^7B^%^22isCorpUser^%^22^%^3Afalse^%^7D; purr-cache=^<K0^<rUS+US-VT^<C_^<Go^<S0; NYT-MPS=0000000c3c6324489d1f596ab6fccbae16cafa957f2820cfc232de046a88f2983e7d75231847410ad719368a3fcd62b4c113ce345e6aed1aa8290afedd3d; NYT-S=28WClUEqbYsk/2tc0CytxdtTUkmpkAZ3yhyN4PPGbjvtm1dbGWcyksd8/Mayx8zYDEjOoea6bgYnR0Iuax90AMVX4OP9myeO3UVXc.uxH6.2LHskgEdkx/Q0DKctcwi2P5IZMElomWjXBvnmPVCuTVr1PoORlAuucOQP8rCo4ZfvOTREDRO.unS000^^^^^^^^CBQSKQiSqM-fBhCKqc-fBhoSMS3OXZvQh7GOX6h5xk2FAP3AIMXSpC4qAh4DGkDUwDcMbERvxKZCQBQFV5MFWXOc-TbclbguditbAxeT2cn6X6LZFynoQyFdsWOS2l7LGgh46JTxKQBrAMdQBHYM; NYT-T=ok; SIDNY=CBQSKQiSqM-fBhCKqc-fBhoSMS3OXZvQh7GOX6h5xk2FAP3AIMXSpC4qAh4DGkDUwDcMbERvxKZCQBQFV5MFWXOc-TbclbguditbAxeT2cn6X6LZFynoQyFdsWOS2l7LGgh46JTxKQBrAMdQBHYM; nyt-auth-method=username; nyt-xwd-hashd=false" -H "Sec-Fetch-Dest: empty" -H "Sec-Fetch-Mode: cors" -H "Sec-Fetch-Site: same-origin" -H "TE: trailers"'
        )
        data = json.loads(request.text)
        print(data)
        
    
    def after_login(self, response):
        if "authentication failed" in response.body:
            print("Login failed")
            self.logger.error("Login failed")
            return
        print("Login successful")