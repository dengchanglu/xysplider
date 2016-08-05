from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.http.cookies import CookieJar
import json
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


# from items import temaSpiderItem

class XieChengSplider(InitSpider):
    name = "xiechengspider"
    allowed_domains = ["ctrip.com"]
    start_urls = ["http://g.ctrip.com/merchant/list/p{num}"]
    login_page = "https://accounts.ctrip.com/member/login.aspx"
    check_login_page = "http://my.ctrip.com/home/myinfo.aspx"
    textCode = ''
    count=0;
    # rule = (Rule(SgmlLinkExtractor(allow='http://g.ctrip.com/merchant/list/p2', callback='parse_content')))

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        # 'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Content-Length': '1684',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'Union=SID=155952&AllianceID=4897&OUID=baidu81|index|||; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; _abtest_userid=6565d804-1e6b-4041-9d72-d4029273fa63; ASP.NET_SessionId=51ia41c3z1nxqlheruoc5eyy; NSC_WT_Bddpvout_443=ffffffff0907902f45525d5f4f58455e445a4a423660; traceExt=campaign=CHNbaidu81&adid=index; adscityen=Chengdu; SMBID=; login_type=0; login_uid=D3CDE3F209DDC44AC55D232A5A5BBEBC; ASP.NET_SessionSvc=MTAuOC4xMTUuNDF8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTQ0OTEzMzMwMjUxNw; __zpspc=9.3.1470295522.1470296925.3%231%7Cbaidu%7Ccpc%7Cbaidu81%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; _jzqco=%7C%7C%7C%7C1470295522442%7C1.189257473.1470190324492.1470295530829.1470296925952.1470295530829.1470296925952.0.0.0.8.8; _gat=1; LoginStatus=0%7c; _ga=GA1.2.547467122.1470190325; _bfa=1.1470190321636.2qj2l9.1.1470209279975.1470295293440.5.38; _bfs=1.9; _bfi=p1%3D100003%26p2%3D100003%26v1%3D38%26v2%3D37',
        'Host': 'accounts.ctrip.com',
        # 'Origin': 'https://accounts.ctrip.com',
        'Referer': 'https://accounts.ctrip.com/member/login.aspx',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
    }
    info_headers = {
        'host': 'g.ctrip.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': '_bfa=1.1451296591644.117epz.1.1470369053219.1470373730336.4.30; __utma=1.916163753.1451296592.1451296592.1451296592.1; _bfi=p1%3D104505%26p2%3D600000312%26v1%3D27%26v2%3D26; SMBID=; LoginStatus=0%7c; login_type=6; login_uid=D3CDE3F209DDC44AA154C0525E34E31A; __zpspc=9.2.1470373734.1470374886.14%234%7C%7C%7C%7C%7C%23; _jzqco=%7C%7C%7C%7C1470369938027%7C1.1828098633.1470369937751.1470374875957.1470374886986.1470374875957.1470374886986.undefined.0.0.16.16; _abtest_userid=83226e41-eec4-45d6-8ba9-fd63324a363e; adscityen=Chengdu; Customer=HAL=ctrip_cn; _ctm_t=ctrip; StartCity_Pkg=PkgStartCity=28; ASP.NET_SessionSvc=MTAuOC45Mi41fDkwOTB8amlucWlhb3xkZWZhdWx0fDE0NDkxMzQ4MjE3NDI; _ga=GA1.2.916163753.1451296592; selectedItem={"province99999":99999,"tags999":999,"rewardtypes99":99,"tagtype99":99,"contient0":0,"country999":999,"city99999":99999}',
        'Connection': 'keep-alive'
    }
    def init_request(self):
        yield Request(url=self.start_urls[0].format(num=1),headers=self.info_headers, callback=self.init)
    def init(self,response):
        self.count = response.xpath('//div[@class="pagination"]/ul/li/a/text()').extract()[10]
        count = int(self.count)
        while count > 0:
            yield Request(url=self.start_urls[0].format(num=count),headers=self.info_headers, callback=self.init)

            count -= 1

    def login(self, response):

        # textCodeUrl = response.selector.xpath('//img').extract()
        self.log(response.body)

        msgCode = raw_input("Please input msgCode!  ")
        self.log('code is ' + msgCode)
        return FormRequest(
            self.login_page,
            headers=self.headers,
            formdata={
                '__EVENTTARGET': '', '__EVENTARGUMENT': '',
                '__VIEWSTATE': '/wEPDwUKMTA0NDI1NDExNw8WAh4DZGRkMtwEAAEAAAD/////AQAAAAAAAAAEAQAAAOIBU3lzdGVtLkNvbGxlY3Rpb25zLkdlbmVyaWMuRGljdGlvbmFyeWAyW1tTeXN0ZW0uU3RyaW5nLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldLFtTeXN0ZW0uU3RyaW5nLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldXQMAAAAHVmVyc2lvbghDb21wYXJlcghIYXNoU2l6ZQADAAiSAVN5c3RlbS5Db2xsZWN0aW9ucy5HZW5lcmljLkdlbmVyaWNFcXVhbGl0eUNvbXBhcmVyYDFbW1N5c3RlbS5TdHJpbmcsIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV1dCAAAAAAJAgAAAAAAAAAEAgAAAJIBU3lzdGVtLkNvbGxlY3Rpb25zLkdlbmVyaWMuR2VuZXJpY0VxdWFsaXR5Q29tcGFyZXJgMVtbU3lzdGVtLlN0cmluZywgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XV0AAAAACxYCZg9kFgQCAg8WAh4Fc3R5bGUFDmRpc3BsYXk6YmxvY2s7FgICAQ8WBB8BBRN2aXNpYmlsaXR5OnZpc2libGU7Hglpbm5lcmh0bWwFNzxpPjwvaT7nmbvlvZXlpLHotKXvvIzor7fkvb/nlKjlhbbku5bmtY/op4jlmajph43or5XjgIJkAhsPZBYCZg8WAh4HVmlzaWJsZWhkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYCBQxjaGtBdXRvTG9naW4FDmNoa0F1dG9Mb2dpbkR5',
                'loginType': '0',
                'hdnToken': 'MjAxNi04LTUgMTE6MDg6MTQ=',
                'hidGohome': 'MjAxNi04LTUgMTE6MDg6MTQ=',
                'hidVerifyCodeLevel': 'N',
                'VerifyCodeFlagDy': 'N',
                'hidMask': 'F', '1': 'on', 'txtUserName': '18328725827', 'txtPwd': '', 'txtCode': '',
                'chkAutoLogin': 'on', 'btnSubmit': "",
                'mobilePhone': '18328725827',
                'txtCodePwd': self.textCode,
                'dyPwd': msgCode,
                'hidToken': 'MjAxNi04LTUgMTE6MDg6MTQ=',
                'hidServerName': 'https://accounts.ctrip.com',
                'hidImgCodeDatahash': 'fEVzvht21470367349081',
                'needCheckServerSession': 'F',
                'cardname': '',
                'hid_cardname': '0',
                'txtCUserName': '',
                'txtCPwd': '',
                'CSVerifyCode': '',
                'txtVerifyCode': '',
                'txtMPwd': '',
                'txtReMPwd': '',
                'txtHPwd': '',
                'txtReHPwd': ''
            },
            callback=self.check_login,
            meta={'handle_httpstatus_all': [400]},
            dont_filter=True)

    def code(self, response):
        return Request(
            url='https://accounts.ctrip.com/member/ajax/AjaxChkBWGAndVerifyCode.ashx?st=sls&username=18328725827&tmp=702',
            headers=self.headers,
            callback=self.sendMsg)

    def sendMsg(self, response):
        # self.log(json.loads(response.body))
        captchaId = json.loads(response.body)['CaptchaId']
        self.log(json.loads(response.body)['Image'])
        self.textCode = raw_input("Please input textCode!  ")
        self.log('code is ' + self.textCode)
        return Request(
            url='https://accounts.ctrip.com/member/ajax/GetDynamicPwdHandler.ashx?mobile=18328725827&captchaId=' + captchaId + '&vcode=' + self.textCode + '&_r=644',
            headers=self.headers,
            callback=self.login)

    def check_login(self, response):
        print response.request.headers
        open("loginRes", 'wb').write(response.body)

        # cookieJar = response.meta.setdefault('cookie_jar', CookieJar())
        # cookieJar.extract_cookies(response, response.request)

        if '{"code":200}' in response.body:
            self.log("=========Successfully logged in.=========")
            # request = Request(url=self.check_login_page, meta={'dont_merge_cookies': True, 'cookie_jar': cookieJar},
            #                   callback=self.parse_directory, dont_filter=True)
            # cookieJar.add_cookie_header(request)
            # return request
        else:
            self.log("=========An error in login occurred.=========")

    def parse_directory(self, response):
        self.log("=========Data is flowing.=========")
        self.log(response.url)
        open("loginPage", 'wb').write(response.body)


    def parse(self, response):

        tmpCookie = response.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
        print 'cookie from login', response.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1]
        cookieHolder = dict(SESSION_ID=tmpCookie)
        newUrl = response.xpath("//div[@class='shop_banner']/a/@href").extract()
        for url in newUrl:
            print response.headers

            request = Request(
                url=self.start_urls[0] + url,
                meta={'cookiejar': response.meta['cookiejar']},
                callback=self.getInfo)
            return request

    def parse_content(self, response):

        # print response.body
        merchantCName = response.xpath('//div[@class="list_R_top_left ellips"]/p/a/text()').extract()
        merchantEName = response.xpath('//div[@class="list_R_top_left ellips"]/p/a/text()').extract()
        for i,cname in enumerate(merchantCName):
            if(i%2==0):
                info = 'merchantCName:' + cname + '------' + 'merchantEName:' + merchantEName[i+1]
                f = open("loginPage", 'a')
                f.write(info.encode('utf-8'))
                f.write("\n")


        # print tmpCookie
        # tm = []
        # for li in tmpCookie:
        #     tm.append(li)
        # cookie=''.join(tm)
        # newUrl = response.xpath("//div[@class='shop_banner']/a/@href").extract()
        # for url in newUrl:
        #     # print cookie
        #     request = Request(
        #         url=self.start_urls[0] + url,
        #         # cookies=tmpCookie,
        #         # headers=response.header,
        #         callback=self.getInfo)
        #     yield request

    def getInfo(self, response):
        merchantCName = response.xpath('//div[@class="merchant_nameL"]/h2/text()').extract()
        merchantEName = response.xpath('//div[@class="merchant_nameL"]/p/text()').extract()
        merchantAddr = response.xpath('//div[@class="conR_shopcon_oneR"]/p')[0].extract()
        merchantTime = response.xpath('//div[@class="conR_shopcon_oneR"]/p')[2].extract()
        merchantTel = response.xpath('//div[@class="conR_shopcon_oneR"]/p')[4].extract()
        merchantWord = response.xpath('//div[@class="shopcon_bottom_word"]/p').extract()
        info = 'merchantCName:' + merchantCName + '------' + 'merchantEName:' + merchantEName + '------' + 'merchantAddr:' + merchantAddr + '------' + 'merchantTime:' + merchantTime + '------' + 'merchantTel:' + merchantTel + '------' + 'merchantWord:' + merchantWord

        self.log(response.body)
