from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.http.cookies import CookieJar
import json
import time


# from items import temaSpiderItem

class JinDongSplider(InitSpider):
    name = "jindongspider"
    allowed_domains = ["jd.com"]
    start_urls = ["http://www.jd.com"]
    login_page = "https://passport.jd.com/new/login.aspx"
    login_service_url = 'https://passport.jd.com/uc/loginService'
    get_jdu_cookie_url = 'https://mercury.jd.com/log.gif?t=www.100000&m=UA-J2011-1&pin=-&uid=1533948524&sid=1533948524|1&v=je%3D0%24sc%3D24-bit%24sr%3D1920x1080%24ul%3Dzh-cn%24cs%3DGBK%24dt%3D%E4%BA%AC%E4%B8%9C-%E6%AC%A2%E8%BF%8E%E7%99%BB%E5%BD%95%24hn%3Dpassport.jd.com%24fl%3D22.0%20r0%24os%3Dlinux%24br%3Dchrome%24bv%3D51.0.2704.63%24wb%3D1471511238%24xb%3D1471511238%24yb%3D1471511238%24zb%3D1%24cb%3D1%24usc%3Ddirect%24ucp%3D-%24umd%3Dnone%24uct%3D-%24lt%3D0%24ct%3D1471511238034%24tad%3D-%24pinid%3D-&ref=&rm=1471511238049'
    get_authcode_url = 'https://passport.jd.com/uc/showAuthCode'
    check_login_page = "https://order.jd.com/center/list.action?search=0&d=2&s=4096"
    textCode = ''
    count = 0;

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

    login_post_data = {'data':''}
    authcodesrc = {'src':''}

    def init_request(self):

        #get loginPage
        yield Request(url=self.login_page, headers=self.get_login_page_headers, callback=self.get_fc)

    def get_fc(self,response):

        #get loginservice interfeace part of cookie
        tmpCookie = response.headers.getlist('Set-Cookie')
        qr = tmpCookie[0].split(";")[0]
        alc = tmpCookie[1].split(";")[0]
        _ntj = tmpCookie[2].split(";")[0]
        self.login_header["Cookie"] = qr + ';' + alc + ';' + _ntj + ';' + self.login_header["Cookie"]
        uuid = response.xpath("//input[@id='uuid']/@value").extract()[0]

        # eid can be null
        eid ='10E9D7BE0885888ECF2D165E6692351007656ED1F26A60094BF4FA7D4B3A0F50714201F029690DB26CAB5EF7455298AA'

        # fp'value ,it has relationship with a browerser and a computer
        fp = 'd029e719e1b0ed5875000eb4cea1214f'
        loginType = response.xpath("//input[@id='loginType']/@value").extract()[0]

        # user's loginName
        loginName = "cjj137783"

        # user' password
        nloginPwd = "cjj31200707"

        # possible value verification code
        authcode = ""

        # these can be null
        machineNet = response.xpath("//input[@id='machineNet']/@value").extract()[0]
        machineCpu = response.xpath("//input[@id='machineCpu']/@value").extract()[0]
        machineDisk = response.xpath("//input[@id='machineDisk']/@value").extract()[0]

        _t = response.xpath("//input[@id='token']/@value").extract()[0]
        arbitrarilyName = response.xpath("//form[@id='formlogin']/input")[8].xpath("//input/@name").extract()[8]
        arbitrarilyValue = response.xpath("//form[@id='formlogin']/input")[8].xpath("//input/@value").extract()[8]

        #convert into formdate
        jsonCong = '{"' + arbitrarilyName + '":"' + arbitrarilyValue + '","uuid":"' +uuid + '","_t":"' + _t + '","loginType":"' + loginType + '","loginname":"' +loginName + '","nloginpwd":"' + nloginPwd + '","loginpwd":"'+nloginPwd+'","authcode":"'+authcode+'","machineNet":"","machineCpu":"","machineDisk":"","eid":"","fp":"'+fp+'"}'
        self.login_post_data['data'] = json.loads(jsonCong)

        #get verification code's url
        self.authcodesrc['src'] = response.xpath("//div[@id='o-authcode']/img/@src2").extract()

        yield Request(url=self.get_jdu_cookie_url, headers=self.jdu_header, callback=self.init)
    def init(self, response):

        # get loginservice interface part of cookie
        tmpCookie = response.headers.getlist('Set-Cookie')
        jdu = tmpCookie[0].split(";")[0]
        self.login_header["Cookie"] = self.login_header["Cookie"] + ';' + jdu

        # call verifycode's interface
        acRequired = FormRequest(self.get_authcode_url,headers=self.login_header, formdata={
            'loginName': self.login_post_data['data']['loginname']},callback=self.get_authcode)  # return ({"verifycode":true})or({"verifycode":false})
        yield acRequired
    def get_authcode(self,response):
        #judge whether the return results for true
        if 'true' in response.body:
            self.get_login_page_headers['Host'] = 'authcode.jd.com'
            self.get_login_page_headers['Referer'] = 'https://passport.jd.com/uc/login'
            request = Request(self.authcodesrc['src'], headers=self.get_login_page_headers,callback=self.authcode)
            return request
        # execute login method
        return self.login()
    def authcode(self,response):
        with open('authcode.jpg', 'wb') as f:
            f.write(response.body)
            self.login_post_data['data']['authcode'] = raw_input("please enter authcode:")
            return self.login()

    def login(self):

        # loginservice interface's queryData, 'r' is random number
        r = "0.40095244084378534"
        version = "2015"

        # execute login method,deal with httpstatus of 200, others httpstatus will throw exception
        request = FormRequest(
            self.login_service_url+'?uuid=' + self.login_post_data['data']['uuid'] + '&&r=' + str(r) + '&version=' + str(version),
            headers=self.login_header,
            formdata=self.login_post_data['data'],
            callback=self.check_login,
            meta={'handle_httpstatus_all': [200], 'dont_merge_cookies': True,},
            dont_filter=True)
        yield request

    def check_login(self, response):
        # login return result
        result = json.loads(str(response.body[1:len(response.body)-1]))
        if(result.get('success','')!=''):
            tmpCookie = response.headers.getlist('Set-Cookie')
            cookie = ''
            #get check_login request part of cookie,but here is not worked
            for tem in tmpCookie:
                cookie += tem.split(";")[0]+';'
            self.login_header["Cookie"] = cookie+self.login_header["Cookie"]
            self.login_header["Host"] = 'www.jd.com'

            # cookiejar manages cookie
            cookieJar = response.meta.setdefault('cookie_jar', CookieJar())
            cookieJar.extract_cookies(response, response.request)

            self.log("=========Successfully logged in.=========")

            # get user's part of order infomation
            request = Request(url=self.check_login_page, meta={'dont_merge_cookies': True,'cookie_jar': cookieJar},
                              callback=self.parse_directory, dont_filter=True)
            cookieJar.add_cookie_header(request)
            return request
        self.log("=========Failing logged in.=========")
        open("loginResF", 'wb').write(response.body)
        _t = result["_t"]
        self.login_post_data["data"]["_t"] = _t
        return self.login()

    def parse_directory(self, response):
        self.log("=========Data is flowing.=========")
        open("loginResF", 'wb').write(response.body)
        for tem in response.xpath(".//div[@id='order02']/div[@class='mc']/table/tbody"):
            #get order number
            order_number = tem.xpath(".//span[@class='number']/a/@id").extract()[0][5:len(tem.xpath(".//span[@class='number']/a/@id").extract()[0])]
            order = tem.xpath(".//tr[@class='tr-bd']/td")
            consignee = order[1].xpath(".//span[@class='txt']/text()").extract()[0]
            print ("\u00a5").decode("unicode-escape")
            order_price = order[2].xpath(".//div[@class='amount']/span/text()").extract()[0].split(("\u00a5").decode("unicode-escape"))[1]
            order_info = '\u8ba2\u5355\u7f16\u53f7\uff1a'.decode("unicode-escape")+str(order_number)+'         \u6536\u8d27\u4eba\uff1a'.decode("unicode-escape")+consignee+'         \u8ba2\u5355\u4ef7\u683c\uff1a'.decode("unicode-escape")+str(order_price)
            f = open("orderData", 'a')
            f.write(order_info.encode('utf-8'))
            f.write("\n")
