import requests
import json
import time
from TANCMS.libs.redisHelper import cacheSet, cacheGet
from scrapy import cmdline
from TANCMS.libs.async_call import async_call


# 监控列表
def requestProgram():
    url = "http://iyanshan.com/spider/program/list"
    beginTime = time.time()
    endTime = time.time() + 86400
    data = {"status": "1", "beginTime": beginTime, "endTime": endTime}
    res = request(url, data)
    return res['data']

# 监控详情
def programDetail(id):
    url = "http://iyanshan.com/spider/program/detail"
    data = {"id": id}
    res = request(url, data)
    return res['detail']

# 网站详情
def networkDetail(id):
    url = "http://iyanshan.com/spider/network/detail"
    data = {"id": id}
    res = request(url, data)
    return res['detail']

# 处理请求
def request(url, data):
    response = requests.post(url=url, json=data)
    res = json.loads(response.content)
    if res['code'] == 0:
        return res['content']
    else:
        raise Exception(res['message'])


# 准备爬虫
def prepareWork():
    try:
        list = requestProgram()
        for program in list:
            detail = programDetail(program['id'])

            cacheSet('program_id', program['id'])
            cacheSet('program_title', program['title'])

            # print(detail)
            # 搜索关键词
            keyWords = detail['keywords']
            keys = []
            for word in keyWords:
                keys.append(word['word'])
            key = ' '.join(keys)

            # 网站
            networks = detail['networks']

            spiders = [] # 需要开始的爬虫
            bloggers = [] # 微博博主
            bars = [] # 贴吧指定吧
            try:
                for network in networks:
                    type = network['type']
                    url = network['url']
                    if network['p_id'] == 0:
                        spiders.append(type)
                        cacheSet(type + '_keyWord', key)
                        cacheSet(type + '_url', url)
                        print(url, key)
                    elif type == 'weibo':
                        # 博主
                        bloggers.append({
                            'stepOne': network['stepOne'],
                            'stepTwo': network['stepTwo']
                        })
                    elif type == 'tieba':
                        bars.append({
                            'bar': network['title'],
                            'url': network['url'],
                            'word': key
                        })
                if len(bloggers) > 0:
                    spiders.append('weiboBlogger')
                    cacheSet('bloggers', json.dumps(bloggers))
                    print(bloggers)
                if len(bars) > 0:
                    spiders.append('tiebaBlogger')
                    cacheSet('bars', json.dumps(bars))
                    print(bars)

                if len(spiders) > 0:
                    # 开始爬虫
                    print('正在爬取方案: ' + detail['title'] + ' 10分钟后下一个方案')
                    cacheSet('spiders', json.dumps(spiders))
                    cmdline.execute('scrapy crawlall'.split())

            except():
                continue
            finally:
                print('next')
                # 开始下一个监控方案前休息10分钟
                # time.sleep(600)
                pass
    except():
        print('except')
    finally:
        print('今日爬虫结束：finally')


if __name__ == '__main__':
    prepareWork()
    # cacheSet('spider_list', '1,2,3,4,5,6')












