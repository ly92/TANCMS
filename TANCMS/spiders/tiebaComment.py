import scrapy
import re
from ..libs.timeHelper import strToTimeStamp
import time
from TANCMS.libs.redisHelper import cacheGet
from ..items import CommentItem
from urllib import parse
from ..libs.ES import isOldComment

class TiebacommentSpider(scrapy.Spider):
    name = 'tiebaComment'

    # 第一步获取详情，得到回帖共多少页
    # 第二步从后向前取得每楼的评论，直到有重复楼

    base_url = ''
    blogs = cacheGet('tiebaComment_blogs')
    blog_id = ''
    page = 1

    def start_requests(self):
        for blog in self.blogs:
            url = blog['url']
            self.blog_id = blog['blog_id']
            self.base_url = url + '?&pn={}'
            yield scrapy.Request(url=url, callback=self.parse_content)

    # 解析贴吧详情
    def parse_content(self, response):
        divs = response.xpath('//*[@id="j_p_postlist"]/div')
        shouldEnd = False
        for div in divs:
            content = div.xpath('.//*[@class="d_post_content j_d_post_content "]/text()').extract_first()
            if not content:
                content = div.xpath('.//*[@class="d_post_content j_d_post_content "]/div[2]/div/text()').extract_first()
            author = div.xpath('.//*[@class="d_name"]/a/text()').extract_first()
            author_url = div.xpath('.//*[@class="d_name"]/a/@href').extract_first()
            author_url = parse.unquote(author_url, encoding='GBK')

            bottom_spans = div.xpath('.//*[@class="post-tail-wrap"]/span').getall()
            if len(bottom_spans) == 4:
                floor = div.xpath('.//*[@class="post-tail-wrap"]/span[3]/text()').extract_first()
                time_str = div.xpath('.//*[@class="post-tail-wrap"]/span[4]/text()').extract_first()
            if len(bottom_spans) == 3:
                floor = div.xpath('.//*[@class="post-tail-wrap"]/span[2]/text()').extract_first()
                time_str = div.xpath('.//*[@class="post-tail-wrap"]/span[3]/text()').extract_first()

            comment = CommentItem()
            comment['time'] = strToTimeStamp(time_str)
            if not isOldComment(self.blog_id, comment['time']):
                comment['blog_id'] = self.blog_id
                comment['content'] = content
                comment['id'] = floor
                comment['author'] = author
                comment['author_url'] = author_url
                yield comment
            elif self.page == 1:
                continue
            else:
                # 结束
                shouldEnd = True
                pass

        if self.page == 1:
            page_a = response.xpath('//*[@class="l_pager pager_theme_4 pb_list_pager"]/a')
            if len(page_a) > 0:
                last_a = page_a[-1]
                title = last_a.xpath('./text()').extract_first()
                if title == '尾页':
                    href = last_a.xpath('./@href').extract_first()
                    pages = re.findall(r'pn=(\d+)', href, re.S)
                    if len(pages) > 0:
                        self.page = pages[0]
                    url = 'https://tieba.baidu.com' + href
                    yield scrapy.Request(url=url, callback=self.parse_content)
        elif not shouldEnd & self.page > 1:
            self.page -= 1
            url = self.base_url.format(self.page)
            yield scrapy.Request(url=url, callback=self.parse_content)











    # 二级评论 tid 帖的ID  pid 评论的ID t 13位时间戳
    comments_url = 'https://tieba.baidu.com/p/comment?tid={}&pid={}&pn=1&t={}'
    # 解析评论的回复, 二级评论
    def parse_comments(self, response):

        # # 评论回复
        # tid = re.findall('thread_id":(.*?),', div.get(), re.S)[0]
        # pid = re.findall('data-pid="(.*?)"', div.get(), re.S)[0]
        # t = int(time.time() * 1000)
        # comment_url = self.comments_url.format(tid, pid, t)
        # yield scrapy.Request(url=comment_url, callback=self.parse_comments)

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
