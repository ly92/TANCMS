import scrapy
from ..items import *
import re
import time
from ..libs.ES import *

class SinanewsSpider(scrapy.Spider):
    name = 'sinaNews'
    base_url = 'https://search.sina.com.cn/?q={}&c=news&from=&col=&range=all&source=&country=&size=10&stime=m-01-01+00%3A00%3A00&etime=m-12-31+23%3A59%3A59&time=m&dpc=0&a=&ps=0&pf=0&page=1'

    def start_requests(self):
        word = '核酸检测'
        yield scrapy.Request(self.base_url.format(word), callback=self.parse)

    def parse(self, response):
        result = response.xpath('//*[@id="result"]')
        for i in range(4, 14):
            item = result.xpath('./div[{}]'.format(i))
            title_a = item.xpath('./h2/a')
            if not title_a:
                title_a = item.xpath('./div/h2/a')
            url = title_a.xpath('./@href').extract_first()
            if 'html?from' in url:
                url = url.replace('?', '')
                url = re.findall('(.*?)from', url, re.S)[0]

            #判断是否已爬取
            if isExitByUrl(url):
                continue

            title = re.findall('target="_blank">(.*?)</a>', title_a.get(), re.S)[0].replace('</font>', '').replace('<font color="red">', '')

            print(url)
            author_time = item.xpath('./h2/span/text()').extract_first()
            if not author_time:
                author_time = item.xpath('./div/h2/span/text()').extract_first()
            author_time = author_time.split(' ')
            author = author_time[0].strip()
            time_str = author_time[1] + ' ' + author_time[2]
            time_date = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')

            item = ArticleItem()
            item['title'] = title
            item['url'] = url
            # item['htmlContent'] = ''
            # item['content'] = ''
            item['author'] = author
            item['time'] = int(time.mktime(time_date))
            yield scrapy.Request(url=url, callback=self.parse_content, meta={'item': item})

        #翻页
        next_page = response.xpath('//*[@id="_function_code_page"]/a[10]/text()').extract_first()
        if next_page == '下一页':
            next_url = response.xpath('//*[@id="_function_code_page"]/a[10]/@href').extract_first()
        else:
            next_url = response.xpath('//*[@id="_function_code_page"]/a[12]/@href').extract_first()
        if next_url:
            # time.sleep(10)
            yield scrapy.Request(url='https://search.sina.com.cn/' + next_url, callback=self.parse)


    # 进入到详情页面 爬取新闻内容
    def parse_content(self, response):

        content = ''.join(response.xpath('//*[@id="artibody" or @id="article"]//p/text()').extract())
        content = re.sub(r'\u3000', '', content)
        content = re.sub(r'[ \xa0?]+', ' ', content)
        content = re.sub(r'\s*\n\s*', '\n', content)
        content = re.sub(r'\s*(\s)', r'\1', content)
        content = ''.join([x.strip() for x in content])

        item = response.meta['item']
        item['htmlContent'] = response.xpath('//*[@id="artibody" or @id="article"]').extract_first()
        item['content'] = content
        item['source'] = '新浪新闻'

        # content_list = response.xpath('//*[@id="artibody" or @id="article"]//p/text()').extract()
        # content = r""
        # for part in content_list:
        #     part = part.strip()
        #     content += part

        yield item
