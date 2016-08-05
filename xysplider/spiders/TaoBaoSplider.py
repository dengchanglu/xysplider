from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule


class TaoBaoSplider(InitSpider):
    name = "taobaospider"
    allowed_domains = ["taobao.com"]
    start_urls = ["https://www.taobao.com/"]
    login_page = "https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fbuyertrade.taobao.com%2Ftrade%2Fitemlist%2Flist_bought_items.htm%3Fspm%3Da21bo.50862.1997525045.2.B30tXI"
    check_login_page = "https://www.taobao.com/"
    # rules = (
    #     Rule(SgmlLinkExtractor(allow=r'-\w+.htm$'),
    #          callback='parse_item', follow=True),
    # )
    headers = {
        "Accept": "image/webp,image/*,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36",
        "Referer": "https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fbuyertrade.taobao.com%2Ftrade%2Fitemlist%2Flist_bought_items.htm%3Fspm%3Da21bo.50862.1997525045.2.B30tXI"
    }

    def parse(self, response):
        filename = response.url.split("/")[-2]
        print filename
        print response.url
        open(filename, 'wb').write(response.body)

    def init_request(self):
        self.log("Initializing...")
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        self.log("Send login request...")
        return FormRequest.from_response(response,
                                         formdata={'TPL_username': '18328725827', 'TPL_password': 'd1015701660',
                                                   'ncoToken': '98346c1be4fcdf500eff120b7656225a7f801a53',
                                                   'slideCodeShow': 'false', 'lang': 'zh_CN', 'loginsite': 0,
                                                   'newlogin': 0,
                                                   'TPL_redirect_url': 'http://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a21bo.50862.1997525045.2.B30tXI',
                                                   'from': 'tb', 'fc': 'default', 'style': 'default',
                                                   'keyLogin': 'false',
                                                   'qrLogin': 'fasle', 'newMini': 'false', 'newMini2': 'false',
                                                   'loginType': 3, 'loginASR': 1, 'loginASRSuc': 1,
                                                   'oslanguage': 'zh-CN', 'sr': '1920*1080',
                                                   'naviVer': 'chrome|51.0270463',
                                                   'um_token': 'HV01PAAZ0ab81217da581e8f579eafe20023d801',
                                                   'ua': '076#Kf2P88PZPhwPDAcaPPPPPKN5XyfYZB+6pmXzZUckaiUerHQZ3hkR4MY5x7t0ZOpRhsb6iUwd4BNo58QaEh+NFRFWS4t0ZC3cPcve/otP9t8JKESPWtZJRB3FVMJXhbVcPPvs60HrgA2Pca5heLrmP8P2hnKksY3cPcve/xtP02QJKESPWtZJRB3FVMJXhh3cPcve/x6PTezJKESPWtZJRB3FVMJXhh3cPcve/o6PTeAxsVikUD54gfwczzoElwQcPcriTavChVxB++N0LMqM/oiubb8rDMXTAnoIg5VcPPvs60HrBP2PUV43XMqpAg4BBmQYQeOezzZIgYOOfZFCtgLmPA2PifI33UCFXt0TToUmT642r8wcPP6EUcQMrkSEt50jgdnifsICP8P8UcIyizGZTZFEN5i176LkQjQcPPjyJFAMyP2PQvMd8Iw0b+rUcctfML47ZXSQbbFBw4p/G1S2zFtAt0giQah7ML47ZXSQbmhrySFCJ8iaRrztS0WsBwCyZhZnYVoxS/eki59wLSt8E/jmrJf+ich0dinRe/5abbFBw4p/G1S2zFtrrHdwHPY7VhnNy7AxS+Y5ySmiAdQ2dWet5IGMmDhkdGi9G3nHTxFGKgtbAQvnr53YnIGxPkCkzYsNL2ziLsD7ZnWujPn/10GtdHe4UfD/eqr5LInnS/C2ZsgsopQ1P8PVrsAPjlECPiWVrwccEIwi+FYVQLcW8A8+rsBc7lECcCyVraqjEIw2whPcPP3BwFg5DBsHP8PwoW+nGCWsFSNAP8PUaO4mB1JegA2Pca5heLrMP8P318+PJqQXbV6AFGpBlCLv5ARBFBJUJohc4A2PuA8cePosOhMtvH6YFRyvZ0HdaJEbWRaCP8P8UcIhagfZTZE9U5i176LkQ8wcPP6EUUe0ZJSEtnWjgdnifsWmP8P2hnKksY3cPcve/x6PTu3xsVikUD54gfwczzoElC3cPcve/o6PwqMJKESPWtZJRB3FVMJXh+QcPcriTyxcFwxB++bBpzqC7rSQSoA7DyqdIZXLmCwcPcI4PLPAPxDNPJuDZkipcQzYo0D2ZNxlULEhwA2PU86cwCPPz73cHHkSHyHqChKgM7jS+d3EK0saP8PFAtBGQzsC+NyyW4qc/DTQf1N7sBXutVxT9xV='},
                                         callback=self.login_response)

    def login_response(self, response):
        open("login", 'wb').write(response.body)
        return Request(url=self.check_login_page, callback=self.check_login_response)

    def check_login_response(self, response):
        open("test", 'wb').write(response.body)
