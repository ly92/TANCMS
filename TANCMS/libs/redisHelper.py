import redis
import json

def cacheSet(key, value):
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True, charset='UTF-8', encoding='UTF-8')
    return r.set(key, value, 43200) # 保留0.5天

def cacheGet(key):
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True, charset='UTF-8', encoding='UTF-8')
    return r.get(key)

if __name__ == '__main__':
    print(cacheSet('test', '哈哈hell——123'))
    print(cacheGet('test'))