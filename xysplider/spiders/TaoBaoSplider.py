from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule


class TaoBaoSplider(InitSpider):
    name = "taobaospider"
    # allowed_domains = ["taobao.com",".alipay.com"]
    start_urls = ["https://www.taobao.com/"]
    login_page = "https://login.taobao.com/member/login.jhtml"
    check_login_page = "https://i.taobao.com/my_taobao.htm"
    umdata_url = 'https://ynuf.alipay.com/service/um.json'
    cna_url = 'https://log.mmstat.com/eg.js'

    # rules = (
    #     Rule(SgmlLinkExtractor(allow=r'-\w+.htm$'),
    #          callback='parse_item', follow=True),
    # )
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0",
        "host":'login.taobao.com',
        'Cookie':''
    }

    umdata_header = {
        'Host':'ynuf.alipay.com',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.5',
        'Accept-Encoding':'gzip, deflate, br',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer':'https://login.taobao.com/member/login.jhtml',
        'Origin':'https://login.taobao.com',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
        'Content-Length':'2882'
    }

    cna_header = {
        'Host':' log.mmstat.com',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Accept':'*/*',
        'Accept-Language':'en-US,en;q=0.5',
        'Accept-Encoding':'gzip, deflate, br',
        'Referer':'https://login.taobao.com/member/login.jhtml',
        'Connection':'keep-alive',
        'If-None-Match':'Z7IxEAqBRBICAXZ0aFlcmDcF',
        'Cache-Control':'max-age=0'
    }

    cookies ={
        'cookie2':'',
        'v':'',
        't':'',
        'token':'',
        'cna':'',
        'collina':'',
        'isg':'AouL13yBWP47X4SsSSBYWpN4GSYS3LtPHlg30_2JikoyHK9-h_Sc8r7ygKcK',
        'umdata':''
    }

    def parse(self, response):
        filename = response.url.split("/")[-2]
        print filename
        print response.url
        open(filename, 'wb').write(response.body)

    def init_request(self):
        self.log("Initializing...")
        yield Request(
            url=self.login_page, headers=self.headers, callback=self.get_cna_cookie)

    def get_login_page(self, response):
        tmpCookie = response.headers.getlist("Set-Cookie")
        cookie2 = tmpCookie[1].split(";")[0]
        v = tmpCookie[0].split(";")[0]
        t = tmpCookie[2].split(";")[0]
        token = tmpCookie[3].split(";")[0]
        self.cookies['cookie2'] = cookie2
        self.cookies['v'] = v
        self.cookies['t'] = t
        self.cookies['token'] = token
        self.log(self.cookies)
        yield FormRequest(
            url=self.umdata_url,method="post", headers=self.umdata_header,formdata={'data':'ENCODE~~V01~~eyJ4diI6IjMuMi43IiwieHQiOiIzM2EyMGYxNTNlZmExMTg2NzRjZmZhNjUzZWZjZGYzZmRjOTdjNmYzIiwiZXRmIjoiYiIsInhhIjoiQ0ZfQVBQX1RCTG9naW5fUEMiLCJ1aWQiOiIiLCJlbWwiOiJBQSIsImV0aWQiOiIiLCJlc2lkIjoiIiwiZXJkIjoiamI5N1Mzb0lWdENLa1o4QnJmNTM5ZDFqTTI2aGljeGxmeDJOZVUyR3FNQT0sSWZ1dEFMMkRVc2VDTzRLd0g3WmZrUnp0Z1lIcGZHdXdvRllmNnRPYzJHaz0iLCJpcHMiOiIxOTIuMTY4LjIuMzgiLCJ0eXBlIjoicGMiLCJuY2UiOnRydWUsIm5wZiI6IkxpbnV4IiwibmFjbiI6Ik1vemlsbGEiLCJuYW4iOiJOZXRzY2FwZSIsIm5sZyI6InpoLUNOIiwic3ciOjE5MjAsInNoIjoxMDgwLCJzYXciOjE4NjMsInNhaCI6MTA1OSwiYnN3IjoxODQ5LCJic2giOjkzNiwiZWxvYyI6Imh0dHBzJTNBJTJGJTJGbG9naW4udGFvYmFvLmNvbSUyRm1lbWJlciUyRmxvZ2luLmpodG1sIiwiZXR6Ijo0ODAsImV0dCI6MTQ3MDkwMDU1NzQxOCwiZWNuIjoiMDE4YjFlNTM1NTM4ZmIxMzdhMmViMDgwNGFlZjNlMjFkMTdkMzJmMSIsImVjYSI6ImNOa3lFRUFLRVdVQ0FYWjBhRm11dDJRTyIsImVzdCI6MCwibXMiOm51bGwsInhzIjoiNzBDRjQwM0FGRkQ3MDdERjA1OUI0ODY5NzdEMDIzQjU2ODgyQzU3QjI5RDE1RTFDMUNCMjQxNUI1NzBFOEIwMTlGNDNCNTBFMjg1QTVCRkRFOTlCRDg0QzdENjQxN0IzMEVCN0U3QzEwRTlGODU5RDJDRjg3ODRGMzcyNkNEN0UyRDlFODFERTlGQUM2QkY3NTE4OEIxMDE5MTEwRTE4QjlBMDY3MDQyQjkxRkZGMUM5OUU5MTY4RDMzQjM3OTAxMjc4RTIxM0IzNzkxRTgzNSIsImZwIjoiUGx1Z0luIiwiZm0iOiJBZG9iZSBMaW51eCIsImZ2IjoiTE5YIDExLDIsMjAyLDYyMSIsImZzYyI6ImNvbG9yIiwiZnN4IjoiMTkyMCIsImZzeSI6IjEwODAiLCJmbGdzIjoiIiwiZmxnIjoiemgtQ04iLCJmb3MiOiI4YzUwZDM1ZWQ2MWY4YzY4MTMxYzRjMzEyZjIwODIxNiIsImZvbnRzIjoiNjE0MTY4OGU5Mzc1NTFkODQ4OTZlNjQ4MWM5MTYwNGYiLCJlZnRzIjoiT2E5YmY2N2E3NmE1ODFkNTQ3ZmYyZTMxYjFlOGU3NmUyLFY3ZTlhZDhjYzg3MDA4MDVlZDA0MmFlZWFiMmMxZWM0ZixDMTJiNGNkNDU4YWQ2NDVkNWIzYWViYTZhM2Y3ZjM3MzcsUGI1NGMzYzQ1MzA1ZDA2ZDNkZmVjNGVkMzAxMjYxM2Q2LFcwNTE4MTQ5MzRiZWE1ZGJjMmEzZmVlNzc2Y2QyZGVhNSxEYzdmMjM2MTI2M2UyOTRlYTRhNGM3YjhlYzMwZTQ3MTksSzkzYWViMzgyYTE3Mjg1MjcyYTBhNjQ4NzQwMGY2YzFkLFIwZTM1YTg2MDgyNTEwZjUzNDU2MWI3NmQ0NjY4MWY3NyxMOTk3NjBkNGEzYTA5M2RlZjM4NDczY2I1OTNiMTQ0MjMsRjJkYWVhYTZjZGY2MDA4OWY0MzVkODhhZDBkZGNkMTU5LCMyYzM2ODY5NjA5YjNmZDFjMDIwNTAyNGNmZTIxZDk1NCxNZGI3ODg3NzI2YmNiNTg3ZWI4OTY5ZjIwOWMyNWIwOGMsRzE2MWYzMmQwOTVkZjdmNGQ5YzhhYWFhYjE2ZTc4YjRiLFQ2NGMwNmVlZjBmYzYwNDM3OThiZDA5MmNjMjI0M2Y2MixBYjhjYWQxNjU3ZTZkYTgzYzQ2ZTdmMThjN2I4MzlmYTQsTmVhOTdkYWJkMjNlODEyZTkzMGQyYzdhYjRlNjRmZjJmLFNmY2U4Yjg0ZDA5ZTBjYjRiMzIyMzFmZjFiZTUwNjQ1ZSxVZWJmNzRjMGFlY2M1NTM3OTk5NTgxNjdhMWMxNDE4YzMsQjBkMGEyOTgxMjA2NjdhYjcyZTAyODY3OTEyMGQ0ZmUyIiwiZWZ0eSI6MCwiZWZjbiI6MTIzLCJlcGwiOjcsImVwIjoiMGRkNzZmNjY4MzVlYzkxYWEzZDBhODUxMTIyZDc0YTUyYjM5Y2JjNCIsImVwbHMiOiJBOGQ0OTE4NWRhMTc5MWUyNWE1NzY5MTMzYjIyYmY5OTVkZGRiNTEzOCxEZGE4NjhhMDUyZTczYmQwZmVhYjBkNDVjMjFiM2YwZTJmZWU2MTk0OCxRMjhlYzcxMTBkNTUwZjJiZWMzZGI3MTA2NDBmZDIyZDg0NDRkMGY4MyxTMjZhYmQwNTk2NTg4NzA4MzY1MTk1YmI3OGY1NTE0ZGI3YTY3MjE4NixWMjA1NWVjMzIzOGEzMmZkNzdjZDJlY2I5NmZkYzE3YWJlZGIzMDNlZSxXMGVkYjViYjk1Mzg3MTcxMTc2YzY2MWIxOThiNTIxZDc2NDg5NjliMyxJNjI3MDYxYTM2MTQ1MTNjMzM3YzhmODQwMDA0YWM2MjFhNTkxNmU3MSIsImVzbCI6ZmFsc2UsImV3Z2wiOiJlMTUwMTI1ODhiOWE2Y2NhMzc1MmY1YmViMjU0ODQ4NjQ0NzkwMDk1In0='}, callback=self.get_umdata_cookie)
        # return FormRequest.from_response(response,
        #                                  formdata={'TPL_username': '18328725827', 'TPL_password': 'd1015701660',
        #                                            'ncoToken': 'c6d030192b8d8d3e37a4f2840f18f6fd1f15b658',
        #                                            'slideCodeShow': 'false', 'lang': 'zh_CN', 'loginsite': 0,
        #                                            'newlogin': 0,
        #                                            'TPL_redirect_url': '',
        #                                            'from': 'tb', 'fc': 'default', 'style': 'default',
        #                                            'keyLogin': 'false',
        #                                            'qrLogin': 'fasle', 'newMini': 'false', 'newMini2': 'false',
        #                                            'loginType': 3, 'loginASR': 1, 'loginASRSuc': 1,
        #                                            'oslanguage': 'zh-CN', 'sr': '1920*1080',
        #                                            'naviVer': 'chrome|51.0270463',
        #                                            'um_token': 'HV01PAAZ0be3f97f7674685957aadc470001edce',
        #                                            'ua': '076#Kf2PR8PzP/zPDAcaPPPPPKN5XyfrZBQmWsP6xUekoOSsNGOz3/3boRohoCtGsBVNOSd4iURbylrZR7taDCz+FRNri7f0e+QcPcrj6VkOjEhlI+Q0hJaQlzlQSEgP+Hs2t+4TpLwcPc0Kg7kLfJBayAzq5xT/BcwEsYTf5y14Pc7gwA2PUMWbvJxulP6mCQ1zno1a2GIrxoUz9+6PqL+YP8PEhodDHzJEvOVxcmhtd+QLULVdzFO0BQPexYwcPc0Kg7kLfJrwyAzq5xT/BcwEsYTf5y14Pc7gBP2PURqh20yC0KFvBuomH786TVXnp6qcY05IAaiqBP2PURqOuXyy0KFvBxRQH786TVXnp6qcY05IAaiqgA2PcPPPav2YP8PJh1DDHzvD6vVxcmOCREVvPcQVzrO0gA2PcPPPavUmP8P2PPPfaL3cPP3Xpu6ZjLHWP8PUu9jZp+dyKA2PcG1Jlkdn8Y3cPP3Xpudo1SVCP8PKvWMPS+aPtSdf0P2PCQPcCAPPrRH+av8yVP2PcAwsDeRUDvAcPC6LFDkSd0eaC4YU6piTKp6jbWmRqYElljegTxwLwAEeueoM5kiTKp6jbWm/u/MUJc+cPCYVrPPPEIwPPsYVQeuW8AuarsBcwUECciYVraqjEIw2wmYVQeuW8A8BwP2PcpkTepat498cPPGgoYN2U8en7oVcPP8PPi2fqP2Pc29JrcQCP8PvjUESSQ+PtS1EsqHRnU1E58QDT8wcPcD2EznSRQi/NTQVeLW6E9WdiP/EPA2PuID0I4SxP4ZbyLGk43uiz3H5x5lJgW+CP8PKvWZ+Nh6PtSnE4A2PsAQaEscxMb1myQYCGEpfMW6Bu3Ubs/y0dqwjVsxCPXDODQlPGVUjo0ARUwQcPcrj6NEvE9hlpRSkLkaQlz1htRXPWHs2t+4TpoVcPP8PPi2fKA2PcG1JX9G9sY3cPP3XpJ6Z4bFaP8Pa0SsDMQmMpRyD7EkvgA2PcPPPav2YP8PJhjfDHzvLSvVxcmOCREVvPcQVzrO0wA2PuMIBvJx278MmCQ1zQrlF2QPMsxsz9hwcPcXKqIkLfDPxyAzq5aspWGaPqCYh5y1mP8P2PPPfaLwcPcXKh2kLfahryAzq5aspWGaPqCYh5y1aP8Pa0SibMOgMpRyDO2pvBP2PURqOTqaL0KFvBvNCH786TVXrGZNG1ubb0ziqwA2PUMWbvJxulg3mCQ1zno1a2GIrxoUz9+6PqL+YP8PEhodDHzJ3eOVxcmhtd+QLULVdzFO0BQPexA=='},
        #                                  callback=self.login_response)
    def get_umdata_cookie(self,response):
        tmpCookie = response.headers.getlist("Set-Cookie")
        umdata = tmpCookie[0].split(";")[0]
        self.cookies['umdata'] = umdata
        yield Request(
            url=self.cna_url, headers=self.cna_header, callback=self.get_cna_cookie)
    def get_cna_cookie(self,response):
        self.log("start login")
        # tmpCookie = response.headers.getlist("Set-Cookie")
        # cna = tmpCookie[0].split(";")[0]
        # self.cookies['cna'] = cna
        return FormRequest(url=self.login_page,headers=self.headers,cookies={'isg':'AouL13yBWP47X4SsSSBYWpN4GSYS3LtPHlg30_2JikoyHK9-h_Sc8r7ygKcK'},method="post",
                                         formdata={'TPL_username': '18328725827', 'TPL_password': 'd1015701660',
                                                   'ncoToken': 'dd1dc4e8114e8ad235252f5aa277b68ef489a407',
                                                   'slideCodeShow': 'false', 'lang': 'zh_CN', 'loginsite': '0',
                                                   'newlogin': '0','gvfdcre':'68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D61317A30322E312E3735343839343433372E352E73354B78787A26663D746F70266F75743D7472756526726564697265637455524C3D6874747073253341253246253246692E74616F62616F2E636F6D2532466D795F74616F62616F2E68746D2533466E656B6F742533443072613378394B325A4755253235334431343730393031383935363536',
                                                   'TPL_redirect_url': 'https://i.taobao.com/my_taobao.htm?nekot=0ra3x9K2ZGU%3D1470901895656','gvfdcname':'10',
                                                   'from': 'tb', 'fc': 'default', 'style': 'default',
                                                   'keyLogin': 'false','keyLogin':'false','qrLogin':'true','newMini':'false','newMini2':'false',
                                                   'qrLogin': 'fasle', 'newMini': 'false', 'newMini2': 'false',
                                                   'loginType': '3', 'loginASR': '1', 'loginASRSuc': '1',
                                                   'oslanguage': 'zh-CN', 'sr': '1920*1080',
                                                   'naviVer': 'firefox|46',
                                                   # 'TPL_password_2':'8cc9fe5d5acf4918b35615477ca07adc9ff059e32f3e88924f6eab1833dd055239827be83b10a5ec5cef7aa58bbe2bfab84a16f9f0d23b2597c21a6cfa7f203d7e6d270f87b7351b2f85f66e3a5a334b18f5618e4ad3a7213ce62bd56d80e8c79a236e431fa82bfe00438ec8601917e8978dccd3644145b474cbe35b8be09bde',
                                                   'um_token': 'HV01PAAZ0be3f97f7674685957aadc470001edce',
                                                   'ua': '076#Kf2PR8PzP/zPDAcaPPPPPKN5XyfrZBQmWsP6xUekoOSsNGOz3/3boRohoCtGsBVNOSd4iURbylrZR7taDCz+FRNri7f0e+QcPcrj6VkOjEhlI+Q0hJaQlzlQSEgP+Hs2t+4TpLwcPc0Kg7kLfJBayAzq5xT/BcwEsYTf5y14Pc7gwA2PUMWbvJxulP6mCQ1zno1a2GIrxoUz9+6PqL+YP8PEhodDHzJEvOVxcmhtd+QLULVdzFO0BQPexYwcPc0Kg7kLfJrwyAzq5xT/BcwEsYTf5y14Pc7gBP2PURqh20yC0KFvBuomH786TVXnp6qcY05IAaiqBP2PURqOuXyy0KFvBxRQH786TVXnp6qcY05IAaiqgA2PcPPPav2YP8PJh1DDHzvD6vVxcmOCREVvPcQVzrO0gA2PcPPPavUmP8P2PPPfaL3cPP3Xpu6ZjLHWP8PUu9jZp+dyKA2PcG1Jlkdn8Y3cPP3Xpudo1SVCP8PKvWMPS+aPtSdf0P2PCQPcCAPPrRH+av8yVP2PcAwsDeRUDvAcPC6LFDkSd0eaC4YU6piTKp6jbWmRqYElljegTxwLwAEeueoM5kiTKp6jbWm/u/MUJc+cPCYVrPPPEIwPPsYVQeuW8AuarsBcwUECciYVraqjEIw2wmYVQeuW8A8BwP2PcpkTepat498cPPGgoYN2U8en7oVcPP8PPi2fqP2Pc29JrcQCP8PvjUESSQ+PtS1EsqHRnU1E58QDT8wcPcD2EznSRQi/NTQVeLW6E9WdiP/EPA2PuID0I4SxP4ZbyLGk43uiz3H5x5lJgW+CP8PKvWZ+Nh6PtSnE4A2PsAQaEscxMb1myQYCGEpfMW6Bu3Ubs/y0dqwjVsxCPXDODQlPGVUjo0ARUwQcPcrj6NEvE9hlpRSkLkaQlz1htRXPWHs2t+4TpoVcPP8PPi2fKA2PcG1JX9G9sY3cPP3XpJ6Z4bFaP8Pa0SsDMQmMpRyD7EkvgA2PcPPPav2YP8PJhjfDHzvLSvVxcmOCREVvPcQVzrO0wA2PuMIBvJx278MmCQ1zQrlF2QPMsxsz9hwcPcXKqIkLfDPxyAzq5aspWGaPqCYh5y1mP8P2PPPfaLwcPcXKh2kLfahryAzq5aspWGaPqCYh5y1aP8Pa0SibMOgMpRyDO2pvBP2PURqOTqaL0KFvBvNCH786TVXrGZNG1ubb0ziqwA2PUMWbvJxulg3mCQ1zno1a2GIrxoUz9+6PqL+YP8PEhodDHzJ3eOVxcmhtd+QLULVdzFO0BQPexA=='},
                                         callback=self.login_response,meta={'handle_httpstatus_all': [400], 'dont_merge_cookies': True,},)
    def login_response(self, response):
        open("login", 'wb').write(response.body)
        tmpCookie = response.headers.getlist("Set-Cookie")
        cookieT = ''
        for cookieM in tmpCookie:
            cookieT+=(cookieM.split(";")[0])+";"
            open("cookie", 'wb').write(cookieT)
        return Request(url=self.check_login_page,headers=response.headers,cookies=cookieT, callback=self.check_login_response,meta={'handle_httpstatus_all': [400], 'dont_merge_cookies': True,},)

    def check_login_response(self, response):
        open("test", 'wb').write(response.body)
