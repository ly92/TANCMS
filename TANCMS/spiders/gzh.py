import scrapy
import requests
import re
import random
import json
from TANCMS.settings import USER_AGENT
from TANCMS.items import ArticleItem
from TANCMS.libs.redisHelper import cacheGet
import time
from TANCMS.libs.ES import isExitArticleByTitle
from TANCMS.libs.timeHelper import formatTime


class GzhSpider(scrapy.Spider):
    name = 'gzh'

    base_url = cacheGet('gzh_url')
    word = cacheGet('gzh_keyWord')
    pn = 1

    def start_requests(self):
        url = self.base_url.format(self.word, self.pn)
        print(url)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        params = self.getCookisParams(response)

        lis = response.xpath('//*[@class="news-list"]/li')
        for li in lis:
            url = 'https://weixin.sogou.com' + li.xpath('./div[2]/h3/a/@href').extract_first()
            articleUrl = self.getArticleUrl(params, url, response.url)
            time.sleep(3)  # 每获取一个文章都停留一会
            print(articleUrl)
            yield scrapy.Request(url=articleUrl, callback=self.detailParse, dont_filter=True)

        page_inner = response.xpath('//*[@class="p-fy"]/a')
        if len(page_inner) > 0 and self.pn < 20:
            last_a = page_inner[-1]
            if last_a.xpath('./text()').extract_first() == '下一页':
                self.pn = self.pn + 1
                url = self.base_url.format(self.word, self.pn)
                print(url)
                time.sleep(3)  # 获取下一页文章前停留一会
                yield scrapy.Request(url=url, callback=self.parse)

    def detailParse(self, response):
        title = response.xpath('//h2[@id="activity-name"]/text()').extract_first().strip()
        if not isExitArticleByTitle(title):
            htmlContent = response.xpath('//div[@id="js_content"]')
            text_lines = htmlContent.xpath('.//span')
            content = ''
            for i, text_line in enumerate(text_lines):
                if text_line:
                    span_text = text_line.xpath('.//text()').extract_first()
                    if span_text:
                        content = content + span_text.strip()
            item = ArticleItem()
            item['title'] = title
            item['url'] = response.url
            item['htmlContent'] = htmlContent.extract_first()
            item['content'] = content
            item['author'] = response.xpath('//*[@id="js_name"]/text()').extract_first().strip()
            item['time'] = self.getTime(response)
            item['source'] = '微信公众号'
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
        return formatTime(ct)


