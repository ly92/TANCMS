import requests
import json
import time
from TANCMS.libs.redisHelper import cacheSet
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
            # print(detail)
            # 搜索关键词
            keyWords = detail['keywords']
            keys = []
            for word in keyWords:
                keys.append(word['word'])
            # print(key)
            key = ' '.join(keys)

            # 网站
            networks = detail['networks']
            try:
                for network in networks:
                    type = network['type']
                    url = network['url']
                    try:
                        startSpider(type, key, url)
                    except(Exception):
                        continue
                    finally:
                        # 当前方案下一个
                        print(network['title'] + '  正在爬取方案: ' + detail['title'])

            except():
                continue
            finally:
                print('正在爬取方案: ' + detail['title'] + ' 准备下一个方案')
                # 开始下一个监控方案前休息1分钟
                # time.sleep(60)
    except():
        print('except')
    finally:
        print('finally')



# 开始爬虫
# @async_call
def startSpider(type, word, url):
    cacheSet(type + '_keyWord', word)
    cacheSet(type + '_url', url)
    print(type, url, word)
    shell = 'scrapy crawl ' + type
    cmdline.execute(shell.split())



if __name__ == '__main__':
    # prepareWork()
    cacheSet('spider_list', '1,2,3,4,5,6')













# if type == 'gzh':
#
# elif type == 'sdWindow':
#
# elif type == 'tieba':
#
# elif type == 'weibo':
#
# elif type == 'toutiao':
#
# elif type == 'sinaNews':
#
# elif type == 'bjh':
#
# elif type == 'tianya':

# print(type, key, url)

# print(network)