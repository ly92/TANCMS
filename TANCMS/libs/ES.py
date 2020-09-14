from elasticsearch import Elasticsearch

es = Elasticsearch(['47.95.145.227:9200'], http_auth=('elastic', 'Super@123'))


def es_index(index, body):
    return es.index(index, body)

def es_query(index, body):
    return es.search(index=index, body=body)

def isExitByTitle(title):
    body = {
        "_source": "title",
        "query": {
            "match_phrase": {
                "title": title
            }
        }
    }
    result = es_query('temp_document', body)
    if result['hits']['total']['value'] > 0:
        return True
    else:
        return False

def isExitByUrl(url):
    body = {
        "_source": "title",
        "query": {
            "match_phrase": {
                "url": url
            }
        }
    }
    result = es_query('temp_document', body)
    if result['hits']['total']['value'] > 0:
        return True
    else:
        return False