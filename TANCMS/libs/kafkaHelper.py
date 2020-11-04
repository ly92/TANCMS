from kafka import KafkaConsumer, KafkaProducer
import time

def productMessage():
    producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')
    msg = "Hello".encode('utf-8')
    producer.send('tancms_iyanshan', msg)
    producer.close()


def consumerMessage():
    consumer = KafkaConsumer('tancms_iyanshan', bootstrap_servers=['127.0.0.1:9092'])
    for msg in consumer:
        recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
        print(recv)

if __name__ == '__main__':
    # productMessage()
    consumerMessage()
