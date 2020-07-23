from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': '47.95.145.227', 'port': '9200'}])


def index(index, body):
    return es.index(index, body)

def query(index, body):
    return es.search(index=index, body=body)