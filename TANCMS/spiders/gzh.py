import scrapy
import requests
import re
import random
import json
from TANCMS.settings import USER_AGENT
from TANCMS.items import GzhItem

class GzhSpider(scrapy.Spider):
    name = 'gzh'
    allowed_domains = ['weixin.sogou.com', 'mp.weixin.qq.com']
    start_urls = ['https://weixin.sogou.com/weixin?query=核酸检查&_sug_type_=&s_from=input&_sug_=n&type=2&page=1&ie=utf8',
                  'https://weixin.sogou.com/weixin?query=核酸检查&_sug_type_=&s_from=input&_sug_=n&type=2&page=2&ie=utf8',
                  'https://weixin.sogou.com/weixin?query=核酸检查&_sug_type_=&s_from=input&_sug_=n&type=2&page=3&ie=utf8',
                  'https://weixin.sogou.com/weixin?query=核酸检查&_sug_type_=&s_from=input&_sug_=n&type=2&page=4&ie=utf8',
                  'https://weixin.sogou.com/weixin?query=核酸检查&_sug_type_=&s_from=input&_sug_=n&type=2&page=5&ie=utf8',
                  'https://weixin.sogou.com/weixin?query=核酸检查&_sug_type_=&s_from=input&_sug_=n&type=2&page=6&ie=utf8',
                  'https://weixin.sogou.com/weixin?query=核酸检查&_sug_type_=&s_from=input&_sug_=n&type=2&page=7&ie=utf8',
                  'https://weixin.sogou.com/weixin?query=核酸检查&_sug_type_=&s_from=input&_sug_=n&type=2&page=8&ie=utf8',
                  'https://weixin.sogou.com/weixin?query=核酸检查&_sug_type_=&s_from=input&_sug_=n&type=2&page=9&ie=utf8',
                  'https://weixin.sogou.com/weixin?query=核酸检查&_sug_type_=&s_from=input&_sug_=n&type=2&page=10&ie=utf8'
                  ]


    template_url = 'https://weixin.sogou.com/weixin?query={}&_sug_type_=&s_from=input&_sug_=n&type=2&page={}&ie=utf8'
    word = '核酸检查'


    def parse(self, response):

        params = self.getCookisParams(response)

        ul = response.xpath('/html/body/div[2]/div[1]/div[3]/ul/li')
        for li in ul:
            url = 'https://weixin.sogou.com' + li.xpath('./div[2]/h3/a/@href').extract_first()
            articleUrl = self.getArticleUrl(params, url, response.url)
            yield scrapy.Request(url=articleUrl, callback=self.detailParse)

        # for page in range(2, 11):
        #     print('12312313123123-----')
        #     yield scrapy.Request(url=self.template_url.format(self.word, page), callback=self.parse)


    def detailParse(self, response):
        htmlContent = response.xpath('//div[@id="js_content"]')
        text_lines = htmlContent.xpath('.//span')
        content = ''
        for i, text_line in enumerate(text_lines):
            if text_line:
                span_text = text_line.xpath('.//text()').extract_first()
                if span_text:
                    content = content + span_text.strip()
        item = GzhItem()
        item['title'] = response.xpath('//h2[@id="activity-name"]/text()').extract_first().strip()
        item['url'] = response.url
        item['htmlContent'] = htmlContent.extract_first()
        item['content'] = content
        item['author'] = response.xpath('//*[@id="js_name"]/text()').extract_first().strip()
        item['time'] = self.getTime(response)
        yield item
        pass



    def getUigsParams(self, response):
        uigs_para = re.findall('var uigs_para = (.*?);', response.text, re.S)[0]
        if 'passportUserId ? "1" : "0"' in uigs_para:
            uigs_para = uigs_para.replace('passportUserId ? "1" : "0"', '0')
        uigs_para = json.loads(uigs_para)
        exp_id = re.findall('uigs_para.exp_id = "(.*?)";', response.text, re.S)[0]
        uigs_para['right'] = 'right0_0'
        uigs_para['exp_id'] = exp_id[:-1]
        return uigs_para

    def getSUID(self, cookie_params):
        url = "https://www.sogou.com/sug/css/m3.min.v.7.css"
        headers = {
            "Accept": "text/css,*/*;q=0.1",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Cookie": "SNUID={}; IPLOC={}".format(cookie_params['SNUID'], cookie_params['IPLOC']),
            "Host": "www.sogou.com",
            "Referer": "https://weixin.sogou.com/",
            "User-Agent": USER_AGENT
        }
        response2 = requests.get(url, headers=headers)
        setCookie = response2.headers['Set-Cookie']
        suid = re.findall('SUID=(.*?);', setCookie, re.S)[0]
        return suid

    def getJSESSIONID(self, cookie_params, requestUrl, setCookie):
        url = "https://weixin.sogou.com/websearch/wexinurlenc_sogou_profile.jsp"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}".format(cookie_params['ABTEST'], cookie_params['SNUID'],
                                                                      cookie_params['IPLOC'],
                                                                      cookie_params['SUID']),
            "Host": "weixin.sogou.com",
            "Referer": requestUrl,
            "User-Agent": USER_AGENT
        }
        response3 = requests.get(url, headers=headers)
        setCookie = response3.headers['Set-Cookie']
        jsessionId = re.findall('JSESSIONID=(.*?);', setCookie, re.S)[0]
        return jsessionId

    def getSUV(self, cookie_params, uigs_para):
        url = "https://pb.sogou.com/pv.gif"
        headers = {
            "Accept": "image/webp,*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Cookie": "SNUID={}; IPLOC={}; SUID={}".format(cookie_params['SNUID'], cookie_params['IPLOC'],
                                                           cookie_params['SUID']),
            "Host": "pb.sogou.com",
            "Referer": "https://weixin.sogou.com/",
            "User-Agent": USER_AGENT
        }
        response4 = requests.get(url, headers=headers, params=uigs_para)
        setCookie = response4.headers['Set-Cookie']
        suv = re.findall('SUV=(.*?);', setCookie, re.S)[0]
        return suv

    def getCookisParams(self, response):
        uigs_para = self.getUigsParams(response)

        setCookieList = response.headers.getlist("Set-Cookie")
        setCookie = ''
        for b in setCookieList:
            setCookie = setCookie + ';' + str(b, encoding="utf-8")

        cookie_params = {
            "ABTEST": re.findall('ABTEST=(.*?);', setCookie, re.S)[0],
            "SNUID": re.findall('SNUID=(.*?);', setCookie, re.S)[0],
            "IPLOC": re.findall('IPLOC=(.*?);', setCookie, re.S)[0],
            "SUID": re.findall('SUID=(.*?);', setCookie, re.S)[0]
        }

        cookie_params['SUID'] = self.getSUID(cookie_params)

        cookie_params['JSESSIONID'] = self.getJSESSIONID(cookie_params, response.url, setCookie)

        cookie_params['SUV'] = self.getSUV(cookie_params, uigs_para)

        return cookie_params

    def get_k_h(self, url):
        b = int(random.random() * 100) + 1
        a = url.find("url=")
        url = url + "&k=" + str(b) + "&h=" + url[a + 4 + 21 + b: a + 4 + 21 + b + 1]
        return url

    def getArticleUrl(self, params, url, request_url):
        url = self.get_k_h(url)

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}; JSESSIONID={}; SUV={}".format(params['ABTEST'],
                                                                                             params['SNUID'],
                                                                                             params['IPLOC'],
                                                                                             params['SUID'],
                                                                                             params['JSESSIONID'],
                                                                                             params['SUV']),
            "Host": "weixin.sogou.com",
            "Referer": request_url,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": USER_AGENT
        }
        response = requests.get(url, headers=headers)

        fragments = re.findall("url \+= '(.*?)'", response.text, re.S)
        article_url = ''
        for i in fragments:
            article_url += i
        return article_url

    def getTime(self, response):
        ct = re.findall('var ct = (.*?);', response.text, re.S)[0]
        ct = ct.replace('"', '')
        return ct


