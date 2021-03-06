import scrapy
import re
from ..libs.timeHelper import strToTimeStamp
import time


class TiebaSpider(scrapy.Spider):
    name = 'tieba'

    # kw = 贴吧名  qw = 关键字
    tie_url = 'https://tieba.baidu.com/f/search/res?ie=UTF-8&isnew=1&kw={}&qw={}&un=&rn=10&sd=&ed=&sm=1&only_thread=1&pn={}'
    ba_url = 'https://tieba.baidu.com/f/search/fm?ie=UTF-8&qw={}&pn={}'
    # tid 帖的ID  pid 评论的ID t 13位时间戳
    comments_url = 'https://tieba.baidu.com/p/comment?tid={}&pid={}&pn=1&t={}'
    word = '核酸检测'
    tieba = '庄河'
    tie_page = 1
    ba_page = 1

    ba_array = []

    # def __init__(self, word, tieba):
    #     print(word, tieba)
    #     self.word = word
    #     self.tieba = tieba

    def start_requests(self):
        url = 'https://tieba.baidu.com/p/6859283852'
        yield scrapy.Request(url=url, callback=self.parse_content)

    # 搜索贴吧
    def ba_requests(self):
        print('开始 ba_requests')

        if self.tieba:
            url = self.ba_url.format(self.tieba, self.ba_page)
            yield scrapy.Request(url=url, callback=self.parse_ba)
        else:
            return self.ba_page

    # 解析贴吧列表
    def parse_ba(self, response):
        print('开始 parse_ba')
        bas = response.xpath('//*[@class="search-forum-list"]/div')
        for ba in bas:
            # print(ba.get())
            name = ba.xpath('.//*[@class="forum-name"]/text()').extract_first()
            followers = ba.xpath('./div[2]/div[2]/span[2]/text()').extract_first()
            ties = ba.xpath('./div[2]/div[2]/span[4]/text()').extract_first()
            memo = ba.xpath('.//*[@class="forum-brief"]').get()
            memo = memo.replace('<div class="directory">', ' ').replace('<div class="forum-brief">', ' ').replace('</div>', ' ')
            self.ba_array.append({'name': name})
        page_a = response.xpath('//*[@class="pager pager-search"]/a')
        for a in page_a:
            title = a.xpath('./text()').extract_first()
            if title == '下一页>':
                url = 'https://tieba.baidu.com' + a.xpath('./@href').extract_first()
                yield scrapy.Request(url=url, callback=self.parse_ba)
                break

    # 搜索贴吧内容
    def tie_requests(self):
        url = self.tie_url.format('', self.word, self.tie_page)
        yield scrapy.Request(url=url, callback=self.parse_tie)

    # 解析贴吧内容列表
    def parse_tie(self, response):
        divs = response.xpath('//*[@class="s_post_list"]/div')
        for div in divs:
            title = div.xpath('./span/a').get()
            a_s = re.findall('<a(.*?)>', title, re.S)
            for a in a_s:
                title = title.replace('<a' + a + '>', '')
            title = title.replace('<em>', '').replace('</em>', '').replace('</a>', '')
            ba = div.xpath('./a[1]/font/text()').extract_first()
            author = div.xpath('./a[2]/font/text()').extract_first()
            time = div.xpath('./font/text()').extract_first()
            time_str = strToTimeStamp(time)
            url = div.xpath('./span/a/@href').extract_first()
            url = 'https://tieba.baidu.com' + re.findall('(.*?)\?', url, re.S)[0]

            yield scrapy.Request(url=url, callback=self.parse_content)

    # 解析贴吧详情
    def parse_content(self, response):

        divs = response.xpath('//*[@id="j_p_postlist"]/div')
        for div in divs:
            content = div.xpath('.//*[@class="d_post_content j_d_post_content "]/text()').extract_first()
            if not content:
                content = div.xpath('.//*[@class="d_post_content j_d_post_content "]/div[2]/div/text()').extract_first()
            author = div.xpath('.//*[@class="d_name"]/a/text()').extract_first()

            bottom_spans = div.xpath('.//*[@class="post-tail-wrap"]/span').getall()
            if len(bottom_spans) == 4:
                floor = div.xpath('.//*[@class="post-tail-wrap"]/span[3]/text()').extract_first()
                time_str = div.xpath('.//*[@class="post-tail-wrap"]/span[4]/text()').extract_first()
            if len(bottom_spans) == 3:
                floor = div.xpath('.//*[@class="post-tail-wrap"]/span[2]/text()').extract_first()
                time_str = div.xpath('.//*[@class="post-tail-wrap"]/span[3]/text()').extract_first()
            print('------------------------------')
            print({'floor':floor, 'author':author, 'time':time_str, 'content':content})

            # 评论回复
            tid = re.findall('thread_id":(.*?),', div.get(), re.S)[0]
            pid = re.findall('data-pid="(.*?)"', div.get(), re.S)[0]
            t = int(time.time() * 1000)
            comment_url = self.comments_url.format(tid, pid, t)
            yield scrapy.Request(url=comment_url, callback=self.parse_comments)

        page_a = response.xpath('//*[@class="l_pager pager_theme_4 pb_list_pager"]/a')
        for a in page_a:
            title = a.xpath('./text()').extract_first()
            if title == '下一页':
                url = 'https://tieba.baidu.com' + a.xpath('./@href').extract_first()
                yield scrapy.Request(url=url, callback=self.parse_content)
                break

    # 解析评论的回复
    def parse_comments(self, response):
        url = response.url
        lis = response.xpath('/html/body/li')
        for li in lis:
            author = li.xpath('./div/a/text()').extract_first()
            content = li.xpath('./div/span/text()').extract_first()
            time_str = li.xpath('./div/div/span[3]/text()').extract_first()
            print({'author':author, 'time':time_str, 'content':content})
        page_a = response.xpath('//*[@class="j_pager l_pager pager_theme_2"]//a')
        url = re.findall('(.*?)&pn', url, re.S)[0]
        for a in page_a:
            title = a.xpath('./text()').extract_first()
            if title == '下一页':
                pn = a.xpath('./@href').extract_first().replace('#', '')
                url = url + '&pn=' + pn + '&t=' + str(int(time.time() * 1000))
                yield scrapy.Request(url=url, callback=self.parse_comments)
                break



