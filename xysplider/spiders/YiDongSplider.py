from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.http.cookies import CookieJar
import json
import time


# from items import temaSpiderItem

class YiDongSplider(InitSpider):
    name = "yidongsplider"
    allowed_domains = ["10086.cn"]
    start_urls = ["http://www.sc.10086.cn/"]
    login_service_url = ''
    check_login_page = "https://order.jd.com/center/list.action?search=0&d=2&s=4096"
    textCode = ''
    count = 0;

    part_location_cookie = {
        'sc': {
            'CmLocation': '280|280',
            'CmProvid': 'sc',
            'login_url': 'https://sc.ac.10086.cn/loginNew/index.jsp',
            'login_interface': 'https://sc.ac.10086.cn/servlet/ssologin',
            'check_login_url': 'http://www.sc.10086.cn/app?service=ajaxDirect/1/fee.FeeInfo/fee.FeeInfo/javascript/&pagename=fee.FeeInfo&eventname=queryFeeinitPage&cond_GOODS_ID=2014080900001741&cond_GOODS_NAME=%E8%AF%9D%E8%B4%B9%E6%9F%A5%E8%AF%A2&ID=undefined&PAGERANDOMID=undefined&ajaxSubmitType=get&ajax_randomcode=0.9217480586298618',
            'Host': 'sc.ac.10086.cn',
            'code_img_url': 'https://sc.ac.10086.cn/loginNew/image_login.jsp?d=' + str(int(time.time())),
            'check_host':'www.sc.10086.cn',
            'redirect_url':''
        }
    }

    get_login_page_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'sc.ac.10086.cn',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0'
    }
    login_header = {
        'Host': 'sc.ac.10086.cn',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://sc.ac.10086.cn/loginNew/index.jsp',
        'Connection': 'keep-alive',
        'Cookie': '',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    code_img_header = {
        'Host': 'sc.ac.10086.cn',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://sc.ac.10086.cn/loginNew/index.jsp',
        'Connection': 'keep-alive',
        'Cookie': '',
    }

    login_post_data = {'data': ''}
    authcodesrc = {'src': ''}

    def init_request(self):
        # get loginPage
        yield Request(url=self.part_location_cookie['sc']['login_url'], headers=self.get_login_page_headers,
                      callback=self.get_code_img)

    def get_code_img(self, response):

        # get loginservice interfeace part of cookie
        tmpCookie = response.headers.getlist('Set-Cookie')
        JSESSIONID = tmpCookie[0].split(";")[0]
        self.login_header["Cookie"] = JSESSIONID + ';' + self.login_header["Cookie"]
        commend_bunch = response.xpath("//form[@id='wtf_2']/input[@name='commend_bunch']/@value").extract()[0]
        query_email = response.xpath("//form[@id='wtf_2']/input[@name='queryEmail']/@value").extract()[0]
        login_value = response.xpath("//form[@id='wtf_2']/input[@name='loginValue']/@value").extract()[0]
        dtype = response.xpath("//form[@id='wtf_2']/input[@name='dtype']/@value").extract()[0]
        pho_nohd = response.xpath("//form[@id='wtf_2']/input[@name='pho_nohd']/@value").extract()[0]
        sid = response.xpath("//form[@id='wtf_2']/input[@name='sid']/@value").extract()[0]
        dispatch = response.xpath("//form[@id='wtf_2']/input[@name='dispatch']/@value").extract()[0]
        psw_type_new = response.xpath("//form[@id='wtf_2']/input[@name='pswTypeNew']/@value").extract()[0]
        act_type = response.xpath("//form[@id='wtf_2']/input[@name='actType']/@value").extract()[0]

        # user's loginName
        phone_no = "13408542996"

        # user' password
        user_passwd = "584521"

        # value verification code
        fakecode = ""

        rememmberMe = ''

        # convert into formdate
        jsonCong = '{"commend_bunch":"' + commend_bunch + '","queryEmail":"' + query_email + '","loginValue":"' + login_value + '","dtype":"' + dtype + '","pho_nohd":"' + pho_nohd + '","sid":"' + sid + '","dispatch":"' + dispatch + '","pswTypeNew":"' + psw_type_new + '","actType":"' + act_type + '","phone_no":"' + phone_no + '","user_passwd":"' + user_passwd + '","fakecode":"' + fakecode + '","rememmberMe":"' + rememmberMe + '"}'
        self.login_post_data['data'] = json.loads(jsonCong)

        self.code_img_header['Cookie'] = self.login_header["Cookie"]
        yield Request(url=self.part_location_cookie['sc']['code_img_url'], headers=self.code_img_header,
                      callback=self.get_auth_code)

    def get_auth_code(self, response):
        with open('authcode.jpg', 'wb') as f:
            f.write(response.body)
            self.login_post_data['data']['fakecode'] = raw_input("please enter authcode:")
            # execute login method
            return self.login()

    def login(self):

        # execute login method,deal with httpstatus of 200, others httpstatus will throw exception
        request = FormRequest(
            self.part_location_cookie['sc']['login_interface'],
            headers=self.login_header,
            formdata=self.login_post_data['data'],
            callback=self.get_my_mobile_cookie,
            meta={'handle_httpstatus_all': [302], 'dont_redirect': True,},
            dont_filter=True)
        yield request

    def get_my_mobile_cookie(self, response):
        tmp_redirect_url = response.headers.getlist('Location')[0]
        self.get_login_page_headers["Host"] = self.part_location_cookie["sc"]['check_host']

        # get user's part of order infomation
        request = Request(url=tmp_redirect_url, headers=self.get_login_page_headers,
                          callback=self.check_login, dont_filter=True,meta = {'dont_redirect': True,'handle_httpstatus_list': [302]})
        return request

    def check_login(self, response):
        self.log("=========Data is flowing.=========")
        tmpCookie = response.headers.getlist('Set-Cookie')
        print tmpCookie
        WADE_ID = tmpCookie[0].split(";")[0]
        cmtokenid = tmpCookie[1].split(";")[0]
        uSign = tmpCookie[2].split(";")[0]
        CmWebtokenid = tmpCookie[3].split(";")[0]
        self.get_login_page_headers['Cookie'] = WADE_ID+';'+cmtokenid+';'+uSign+';'+CmWebtokenid
        request = Request(url=self.part_location_cookie['sc']['check_login_url'], headers=self.get_login_page_headers,
                          callback=self.parse_directory, dont_filter=True)
        return request
    def parse_directory(self,response):
        data = json.loads(response.body.split("![CDATA[[")[1].split("]]]")[0])
        open("billingInfo", 'wb').write(data["OUT_MSG"].encode('utf-8')+"\n\n")
