import scrapy
import toml
import json
from scrapy_splash import SplashRequest, SplashFormRequest


lua_script = '''
function main(splash, args)
    splash:init_cookies(splash.args.cookies)
    
    assert(splash:go(args.url))
    assert(splash:wait(1))
    
    splash:set_viewport_full()
    
    local email_input = splash:select('input[name=email]')
    local email = args.email
    email_input:send_text(email)
    assert(splash:wait(1))
    
    local email_submit = splash:select('button[type=submit]')
    email_submit:click()
    assert(splash:wait(3))

    local password_input = splash:select('input[id=password]')
    local password = args.password
    password_input:send_text(password)
    assert(splash:wait(1))

    local password_submit = splash:select('button[type=submit]')
    password_submit:click()
    assert(splash:wait(3))

    return {
        html = splash:html(),
        url = splash:url(),
        cookies = splash:get_cookies(),
        }

    end
'''

def get_secrets():
    secret_path = 'secrets.toml'
    secrets = toml.load(secret_path)
    username = secrets['NYTXW']['username']
    password = secrets['NYTXW']['password']

    return username, password

class NytxwSpider(scrapy.Spider):
    name = "NYTXW"
 
    def start_requests(self):
        email, password = get_secrets()
        login_url = f'https://myaccount.nytimes.com/auth/enter-email?redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fcrosswords%2Fgame%2Fdaily%2F1993%2F11%2F21&response_type=cookie&client_id=games&application=crosswords&asset=navigation-bar'
        yield SplashRequest(url=login_url,
                            callback=self.start_scraping,
                            endpoint='execute',
                            args={
                                'width': 1000,
                                'lua_source' : lua_script,
                                'email': email,
                                'password': password,
                                'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
                            }
                            )
    
    def start_scraping(self, response):
        cookies_dict = {cookie['name']: cookie['value'] for cookie in response.data['cookies']}
        url = 'https://www.nytimes.com/crosswords/game/daily/1993/11/21?login=email&auth=login-email'
        yield scrapy.Request(url=url, cookies=cookies_dict, callback=self.parse)

    def parse(self, response):
        request = scrapy.Request.from_curl(
             'curl "https://www.nytimes.com/svc/crosswords/v6/puzzle/daily/1993-11-21.json" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0" -H "Accept: */*" -H "Accept-Language: en-US,en;q=0.5" -H "Accept-Encoding: gzip, deflate, br" -H "nyt-s: 28WClUEqbYsk/2tc0CytxdtTUkmpkAZ3yhyN4PPGbjvtm1dbGWcyksd8/Mayx8zYDEjOoea6bgYnR0Iuax90AMVX4OP9myeO3UVXc.uxH6.2LHskgEdkx/Q0DKctcwi2P5IZMElomWjXBvnmPVCuTVr1PoORlAuucOQP8rCo4ZfvOTREDRO.unS000^^^^^^^^CBQSKQiSqM-fBhCKqc-fBhoSMS3OXZvQh7GOX6h5xk2FAP3AIMXSpC4qAh4DGkDUwDcMbERvxKZCQBQFV5MFWXOc-TbclbguditbAxeT2cn6X6LZFynoQyFdsWOS2l7LGgh46JTxKQBrAMdQBHYM" -H "Content-type: application/x-www-form-urlencoded" -H "DNT: 1" -H "Connection: keep-alive" -H "Referer: https://www.nytimes.com/crosswords/game/daily/1993/11/21?login=email&auth=login-email" -H "Cookie: nyt-a=lMjWZaRnxmJF81gXE8abJL; nyt-gdpr=0; nyt-purr=cfhhpfhhhckfhd; edu_cig_opt=^%^7B^%^22isEduUser^%^22^%^3Afalse^%^7D; nyt-jkidd=uid=0&lastRequest=1676916441888&activeDays=^%^5B0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C0^%^2C1^%^5D&adv=1&a7dv=1&a14dv=1&a21dv=1&lastKnownType=anon&newsStartDate=&entitlements=; b2b_cig_opt=^%^7B^%^22isCorpUser^%^22^%^3Afalse^%^7D; purr-cache=^<K0^<rUS+US-VT^<C_^<Go^<S0; NYT-MPS=0000000c3c6324489d1f596ab6fccbae16cafa957f2820cfc232de046a88f2983e7d75231847410ad719368a3fcd62b4c113ce345e6aed1aa8290afedd3d; NYT-S=28WClUEqbYsk/2tc0CytxdtTUkmpkAZ3yhyN4PPGbjvtm1dbGWcyksd8/Mayx8zYDEjOoea6bgYnR0Iuax90AMVX4OP9myeO3UVXc.uxH6.2LHskgEdkx/Q0DKctcwi2P5IZMElomWjXBvnmPVCuTVr1PoORlAuucOQP8rCo4ZfvOTREDRO.unS000^^^^^^^^CBQSKQiSqM-fBhCKqc-fBhoSMS3OXZvQh7GOX6h5xk2FAP3AIMXSpC4qAh4DGkDUwDcMbERvxKZCQBQFV5MFWXOc-TbclbguditbAxeT2cn6X6LZFynoQyFdsWOS2l7LGgh46JTxKQBrAMdQBHYM; NYT-T=ok; SIDNY=CBQSKQiSqM-fBhCKqc-fBhoSMS3OXZvQh7GOX6h5xk2FAP3AIMXSpC4qAh4DGkDUwDcMbERvxKZCQBQFV5MFWXOc-TbclbguditbAxeT2cn6X6LZFynoQyFdsWOS2l7LGgh46JTxKQBrAMdQBHYM; nyt-auth-method=username; nyt-xwd-hashd=false" -H "Sec-Fetch-Dest: empty" -H "Sec-Fetch-Mode: cors" -H "Sec-Fetch-Site: same-origin" -H "TE: trailers"'
        )
        data = json.loads(request)
        with open('response.json', 'w') as f:
            f.write(data)

    