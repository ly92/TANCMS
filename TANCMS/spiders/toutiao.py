import scrapy
import time
import json
from ..items import ArticleItem
import re
from ..libs.ES import isExitByUrl
import requests
from TANCMS.libs.redisHelper import cacheGet

class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    # base_url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset={}&format=json&keyword={}&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp={}&_signature=oHuGVAAgEBC2A4AvKc6seKB6x0AAP9zO0qofiJ3FhiTBQ3gNCJ8.vSaBmrGj4SZdrsFpWFt51cjKW9XeH14ZmxRBirFuRvjBtWG3GI-FQqbTIZOgYbTf34u5fGNLTWPcPYU'
    offset = 0
    session = requests.Session()
    nodejs_server = 'http://127.0.0.1:8000/toutiao'

    base_url = cacheGet('toutiao_url')
    word = cacheGet('toutiao_keyWord')

    def start_requests(self):
        ts = int(time.time() * 1000)
        url = self.base_url.format(self.offset, self.word, ts)
        # url = 'https://www.toutiao.com/a6820727747896148487/'
        yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):
        data = json.loads(response.text)['data']
        has_more = json.loads(response.text)['has_more']
        for item in data:
            # 舍弃悟空问答
            if 'abstract' in item and 'answer_count' not in item and 'app_info' in item and 'db_name' in item['app_info'] and item['app_info']['db_name'] == 'SITE':
                article = ArticleItem()
                article['title'] = item['title']
                article['url'] = 'https://www.toutiao.com/a' + item['item_id']

                if isExitByUrl(article['url']):
                    continue
                # article['url'] = item['article_url']
                article['author'] = item['media_name']
                article['source'] = '今日头条'
                article['time'] = item['create_time']
                content = self.parse_content(article['url'])
                article['content'] = content
                article['htmlContent'] = ''
                if len(content) > 0:
                    yield article

        if has_more:

            self.offset = self.offset + 20
            ts = int(time.time() * 1000)
            url = self.base_url.format(self.offset, self.word, ts)
            time.sleep(5)  # 获取下一页文章前停留一会
            yield scrapy.Request(url, callback=self.parse)


    def parse_content(self, url):
        print(url)
        headers = {
            'authority': 'www.toutiao.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        try:
            res = self.session.get(url=url, headers=headers, verify=False)
            content = self.get_content(res.text)
            if content:
                return content
            else:
                # 在 response 中获取 key为：__ac_nonce 的值，用来生成 __ac_signature
                res = self.session.get(url=url, headers=headers, verify=False)
                nonce = res.cookies['__ac_nonce']
                userAgent = headers['user-agent']
                params = {
                    'nonce': nonce,
                    'url': url,
                    'userAgent': userAgent
                }
                signature = requests.get(self.nodejs_server, params=params).text

                self.session.cookies['__ac_signature'] = signature
                res = self.session.get(url=url, headers=headers, verify=False)
                return self.get_content(res.text)
        except:
            return ''

    def get_content(self, text):
        articleInfos = re.findall('articleInfo: {(.*?)groupId', text, re.S)
        if len(articleInfos) > 0:
            contents = re.findall('content: (.*?)slice', articleInfos[0], re.S)
            if len(contents) > 0:
                content = contents[0]
                content = content.replace('&nbsp;', ' ').replace('\\u003C', '<').replace('\\u003E', '>').replace(
                    '&amp;', '&').replace('&quot;', '').replace('\\u002F', '/').replace('<br>', '').replace('收藏 举报', '')
                ps = re.findall('<p>(.*?)</p>', content, re.S)
                content = "\n".join(ps)
                return content
        else:
            return ''

