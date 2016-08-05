from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.http.cookies import CookieJar
# from items import temaSpiderItem

class fanjianSplider(InitSpider):
    name = "fanjianspider"
    allowed_domains = ["fanjian.net"]
    start_urls = ["http://www.fanjian.net/user/login"]
    login_page = "http://www.fanjian.net/user/login"
    check_login_page = "http://www.fanjian.net"

    headers = {
        'Accept': 'application / json, text / javascript, * / *; q = 0.01',
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': 'zh-CN, zh;q = 0.8',
        'Connection': 'keep-alive',
        'Content-Length': '27',
        'Content-Type': 'application/x-www-form-urlencoded;charset = UTF-8',
        'Host': 'www.fanjian.net',
        'Origin': 'http://www.fanjian.net',
        'Referer': 'http://www.fanjian.net/',
        'User-Agent': 'Mozilla / 5.0(X11;Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 51.0.2704.63 Safari / 537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def init_request(self):
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        return FormRequest(self.login_page,
                                         formdata={'email': 'd1015701660', 'passwd': 'd1015701660'},
                                         callback=self.check_login,
                                         dont_filter=True)

    def check_login(self, response):
        cookieJar = response.meta.setdefault('cookie_jar', CookieJar())
        cookieJar.extract_cookies(response, response.request)
        if '{"code":200}' in response.body:
            self.log("=========Successfully logged in.=========")
            request = Request(url=self.check_login_page,meta = {'dont_merge_cookies': True, 'cookie_jar': cookieJar}, callback=self.parse_directory, dont_filter=True)
            cookieJar.add_cookie_header(request)
            return request
        else:
            self.log("=========An error in login occurred.=========")

    def parse_directory(self, response):
        self.log("=========Data is flowing.=========")
        self.log(response.url)
        open("loginPage", 'wb').write(response.body)