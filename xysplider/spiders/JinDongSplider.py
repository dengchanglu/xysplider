from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.http.cookies import CookieJar
import json
import time
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import random


# from items import temaSpiderItem

class JinDongSplider(InitSpider):
    name = "jindongspider"
    allowed_domains = ["jd.com"]
    start_urls = ["http://www.jd.com"]
    login_page = "https://passport.jd.com/new/login.aspx"
    login_service_url = 'https://passport.jd.com/uc/loginService'
    get_jdu_cookie_url = 'https://mercury.jd.com/log.gif?t=www.100000&m=UA-J2011-1&pin=-&uid=1533948524&sid=1533948524|1&v=je%3D0%24sc%3D24-bit%24sr%3D1920x1080%24ul%3Dzh-cn%24cs%3DGBK%24dt%3D%E4%BA%AC%E4%B8%9C-%E6%AC%A2%E8%BF%8E%E7%99%BB%E5%BD%95%24hn%3Dpassport.jd.com%24fl%3D22.0%20r0%24os%3Dlinux%24br%3Dchrome%24bv%3D51.0.2704.63%24wb%3D1471511238%24xb%3D1471511238%24yb%3D1471511238%24zb%3D1%24cb%3D1%24usc%3Ddirect%24ucp%3D-%24umd%3Dnone%24uct%3D-%24lt%3D0%24ct%3D1471511238034%24tad%3D-%24pinid%3D-&ref=&rm=1471511238049'
    get_authcode_url = 'https://passport.jd.com/uc/showAuthCode'
    check_login_page = "https://order.jd.com/center/list.action"
    textCode = ''
    count = 0;
    # rule = (Rule(SgmlLinkExtractor(allow='http://g.ctrip.com/merchant/list/p2', callback='parse_content')))

    get_login_page_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'passport.jd.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0'
    }
    login_header = {
        'Host': 'passport.jd.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://passport.jd.com/new/login.aspx',
        'Connection': 'keep-alive',
        'Cookie': '__jda=122270672.1791980631.1471578832.1471578832.1471578832.1;__jdb=122270672.1.1791980631|1.1471578832;__jdc=122270672;__jdv=122270672|direct|-|none|-;3AB9D23F7A4B3C9B=10E9D7BE0885888ECF2D165E6692351007656ED1F26A60094BF4FA7D4B3A0F50714201F029690DB26CAB5EF7455298AA;__jrda=1;__jrdb='+str(int(time.time())),
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type':'application/x-www-form-urlencoded; charset=utf-8'
    }
    jdu_header = {
        'Host': 'mercury.jd.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://passport.jd.com/new/login.aspx',
        'Connection': 'keep-alive',
        'Cookie': '__jda=122270672.1791980631.1471578832.1471578832.1471578832.1;__jdb=122270672.1.1791980631|1.1471578832;__jdc=122270672;__jdv=122270672|direct|-|none|-',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
    }
    get_fc_header = {
        'Host':'payrisk.jd.com',
        'User-Agent':' Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.5',
        'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
        'Referer':'https://passport.jd.com/new/login.aspx',
        'Content-Length':'18083',

    }

    login_post_data = {'data':''}
    authcodesrc = {'src':''}

    def init_request(self):
        yield Request(url=self.login_page, headers=self.get_login_page_headers, callback=self.get_fc)
    def get_fc(self,response):
        tmpCookie = response.headers.getlist('Set-Cookie')
        qr = tmpCookie[0].split(";")[0]
        alc = tmpCookie[1].split(";")[0]
        _ntj = tmpCookie[2].split(";")[0]
        self.login_header["Cookie"] = qr + ';' + alc + ';' + _ntj + ';' + self.login_header["Cookie"]
        uuid = response.xpath("//input[@id='uuid']/@value").extract()[0]
        eid ='10E9D7BE0885888ECF2D165E6692351007656ED1F26A60094BF4FA7D4B3A0F50714201F029690DB26CAB5EF7455298AA'
        fp = 'd029e719e1b0ed5875000eb4cea1214f'
        loginType = response.xpath("//input[@id='loginType']/@value").extract()[0]

        loginName = "18328725827"
        nloginPwd = "cjj31200707"
        authcode = ""
        machineNet = response.xpath("//input[@id='machineNet']/@value").extract()[0]

        machineCpu = response.xpath("//input[@id='machineCpu']/@value").extract()[0]

        machineDisk = response.xpath("//input[@id='machineDisk']/@value").extract()[0]
        _t = response.xpath("//input[@id='token']/@value").extract()[0]

        arbitrarilyName = response.xpath("//form[@id='formlogin']/input")[8].xpath("//input/@name").extract()[8]
        arbitrarilyValue = response.xpath("//form[@id='formlogin']/input")[8].xpath("//input/@value").extract()[8]
        # "eid":"' + eid + '", "fp":"' +fp + '",,"machineNet":"' + machineNet + '","machineCpu":"' +machineCpu + '","machineDisk":"' + machineDisk+ '"
        jsonCong = '{"' + arbitrarilyName + '":"' + arbitrarilyValue + '","uuid":"' +uuid + '","_t":"' + _t + '","loginType":"' + loginType + '","loginname":"' +loginName + '","nloginpwd":"' + nloginPwd + '","loginpwd":"'+nloginPwd+'","authcode":"'+authcode+'","machineNet":"","machineCpu":"","machineDisk":"","eid":"","fp":"'+fp+'"}'
        print "++++++++++++++++++++++++++++++++++++++++++++++++++"
        print (jsonCong)
        print "++++++++++++++++++++++++++++++++++++++++++++++++++"

        # jtext = json.dumps(jsonCong)
        self.login_post_data['data'] = json.loads(jsonCong)

        self.authcodesrc['src'] = response.xpath("//div[@id='o-authcode']/img/@src2").extract()

        # yield Request(url=self.get_eid_url, headers=self.get_login_page_headers, callback=self.init)
        yield Request(url=self.get_jdu_cookie_url, headers=self.jdu_header, callback=self.init)
    def init(self, response):
        tmpCookie = response.headers.getlist('Set-Cookie')
        jdu = tmpCookie[0].split(";")[0]
        self.login_header["Cookie"] = self.login_header["Cookie"] + ';' + jdu
        acRequired = FormRequest(self.get_authcode_url,headers=self.login_header, formdata={
            'loginName': self.login_post_data['data']['loginname']},callback=self.get_authcode)  # return ({"verifycode":true})or({"verifycode":false})
        yield acRequired
    def get_authcode(self,response):
        if 'true' in response.body:
            self.headers['Host'] = 'authcode.jd.com'
            self.headers['Referer'] = 'https://passport.jd.com/uc/login'
            response = self.session.get(self.authcodesrc['src'], headers=self.headers)
            with open('authcode.jpg', 'wb') as f:
                f.write(response.content)
                self.login_post_data['data']['authcode'] = input("plz enter authcode:")
        return self.login()
    def login(self):

        r = "0.40095244084378534"
        version = "2015"
        # data = json.loads(self.login_post_data['data'])
        print self.login_header["Cookie"]
        request = FormRequest(
            self.login_service_url+'?uuid=' + self.login_post_data['data']['uuid'] + '&&r=' + str(r) + '&version=' + str(version),
            headers=self.login_header,
            # cookies=self.login_header["Cookie"],
            formdata=self.login_post_data['data'],
            callback=self.check_login,
            meta={'handle_httpstatus_all': [400], 'dont_merge_cookies': True,},
            dont_filter=True)
        yield request

    def check_login(self, response):
        result = json.loads(str(response.body[1:len(response.body)-1]))
        if(result.get('success','')!=''):
            tmpCookie = response.headers.getlist('Set-Cookie')
            cookie = ''
            for tem in tmpCookie:
                cookie += tem.split(";")[0]+';'


            self.login_header["Cookie"] = cookie+self.login_header["Cookie"]
            self.login_header["Host"] = 'www.jd.com'
            print self.login_header["Cookie"]
            cookieJar = response.meta.setdefault('cookie_jar', CookieJar())
            cookieJar.extract_cookies(response, response.request)
            # print cookieJar.extract_cookies

            self.log("=========Successfully logged in.=========")
            request = Request(url=self.check_login_page, meta={'dont_merge_cookies': True,'cookie_jar': cookieJar},
                              # headers=response.headers,
                              callback=self.parse_directory, dont_filter=True)
            cookieJar.add_cookie_header(request)
            return request
        self.log("=========Failing logged in.=========")
        open("loginResF", 'wb').write(response.body)
        _t = result["_t"]
        data = self.login_post_data["data"]["_t"] = _t
        return self.login()

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
        for i, cname in enumerate(merchantCName):
            if (i % 2 == 0):
                info = 'merchantCName:' + cname + '------' + 'merchantEName:' + merchantEName[i + 1]
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
