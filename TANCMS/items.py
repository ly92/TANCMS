# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    htmlContent = scrapy.Field()
    source = scrapy.Field()

class ImageItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()

class BlogItem(scrapy.Item):
    blog_id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    author_id = scrapy.Field()
    author_url = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()

    bar = scrapy.Field()
    bar_url = scrapy.Field()

class CommentItem(scrapy.Item):
    comment_id = scrapy.Field()
    blog_id = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    author_id = scrapy.Field()
    author_url = scrapy.Field()
    author_url = scrapy.Field()