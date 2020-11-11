from elasticsearch import Elasticsearch, helpers
from TANCMS.libs.redisHelper import cacheGet
from TANCMS.libs.async_call import async_call
import datetime

es = Elasticsearch(['47.95.145.227:9200'], http_auth=('tancms', 'Tan123456'))


def es_index(index, body):
    return es.index(index, body)

def es_query(index, body):
    return es.search(index=index, body=body)

def es_update(index, id, body):
    return es.update(index=index, id=id, body=body)

def es_multi_index(body):
    return helpers.bulk(es, body)


def isExitArticleByTitle(title):
    body = {
        "query": {
            "match_phrase": {
                "title": title
            }
        }
    }
    result = es_query('temp_document', body)
    if result['hits']['total']['value'] > 0:
        addProgram(result['hits']['hits'])
        return True
    else:
        return False

def isExitArticleByUrl(url):
    body = {
        "query": {
            "match_phrase": {
                "url": url
            }
        }
    }
    result = es_query('temp_document', body)
    if result['hits']['total']['value'] > 0:
        addProgram(result['hits']['hits'])
        return True
    else:
        return False

def isExitBlogByUrl(url):
    body = {
        "query": {
            "match_phrase": {
                "url": url
            }
        }
    }
    result = es_query('temp_blog', body)
    if result['hits']['total']['value'] > 0:
        addProgram(result['hits']['hits'])
        return True
    else:
        return False

def isOldComment(blog_id, time):
    return False


@async_call
def addProgram(hits):
    program_id = cacheGet('program_id')
    program_title = cacheGet('program_title')
    temp = []
    for hit in hits:
        programs = hit['_source']['programs']
        hasProgram = False
        for program in programs:
            if program['programId'] == program_id:
                hasProgram = True
                break
        if not hasProgram:
            temp.append(hit['_id'])
    if len(temp) > 0:
        for id in temp:
            body = {
                "script": {
                    "source": "ctx._source.programs.add(params.tag)",
                    "params": {
                        "tag": {
                            "programId": program_id,
                            "programTitle": program_title
                        }
                    }
                }
            }
            es_update(hit['_index'], id, body)




def test_bulk():
    actions = []
    for i in range(10):
        actions.append({
            "_op_type": "index", #操作 index update create delete
            "_index": "temp_document",
            "_source": {
                "addTime": datetime.time,
                "creationTime": "",
                "author": "FM1007福建交通广播",
                "content": "昨晚（9日），新疆维吾尔自治区人民政府新闻办公室召开第十场新闻发布会，自治区党委宣传部副部长、新闻发言人王武龙通报，11月8日0时至8日24时，新疆维吾尔自治区（含新疆生产建设兵团）无新增新冠肺炎确诊病例和无症状感染者，这是此次喀什疏附县疫情发生以来，首次确诊病例和无症状感染者零新增。",
                "programs": [
                    {
                        "programId": i,
                        "programTitle": "核酸检测"
                    }
                ],
                "htmlContent": "",
                "source": "微信公众号",
                "title": "8717人核酸检测结果公布！钟南山最新提醒",
                "url": "https://mp.weixin.qq.com/s?src=11&timestamp=1604991001&ver=2697&signature=WixTb*3BETJ-vsZlmEs0cDa8sEcxa*KWcOKKGcIvI9gn3bHRE1UU5jWFq3vp8vMvf17kv2RTE1a1QQikz0rA6rTUhoFpwHaDf0-PxGkluLW20L54dPBZDo1*g5iK6XiU&new=1"
            }
        })

    for i in range(2):
        actions.append({
            "_op_type": "index",
            "_index": "temp_blog",
            "_source": {
                "blog_comments_relation": {
                    "name": "blog"
                },
                "source": "微信公众号",
                "title": "8717人核酸检测结果公布！钟南山最新提醒",
                "url": "1231231"
            }
        })

    es_multi_index(actions)

if __name__ == '__main__':
    # test_bulk()
    print(datetime.date)