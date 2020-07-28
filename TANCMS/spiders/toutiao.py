import scrapy
import time
import json
from ..items import ArticleItem
import re
import urllib
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from ..libs.ES import isExitByUrl

class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    base_url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset={}&format=json&keyword={}&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp={}&_signature=oHuGVAAgEBC2A4AvKc6seKB6x0AAP9zO0qofiJ3FhiTBQ3gNCJ8.vSaBmrGj4SZdrsFpWFt51cjKW9XeH14ZmxRBirFuRvjBtWG3GI-FQqbTIZOgYbTf34u5fGNLTWPcPYU'
    offset = 0
    word = '核酸检测'

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
            if 'abstract' in item and 'answer_count' not in item:
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

                # yield scrapy.Request(url=article['url'], callback=self.parse_content, meta={'item': article})
        if has_more:
            self.offset = self.offset + 20
            ts = int(time.time() * 1000)
            url = self.base_url.format(self.offset, self.word, ts)
            yield scrapy.Request(url, callback=self.parse)


    def parse_content(self, url):
        print(url)

        options = Options()
        options.add_argument('-headless')
        driver = Firefox(executable_path='/usr/local/Cellar/geckodriver/0.26.0/bin/geckodriver',
                         firefox_options=options)
        content = ''
        try:
            driver.get(url)
            time.sleep(2)
            content = driver.find_element_by_xpath(
                '//div[@class="article-box"]')
            content = content.text
        except:
            print('--------------------')
        driver.close()
        return content




