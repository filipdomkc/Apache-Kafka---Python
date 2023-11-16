#Synchronous send

from time import sleep
from json import dumps
from kafka import KafkaProducer

topic_name = 'synchronous-send'
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer = lambda x: dumps(x).encode('utf-8'))

for e in range (100):
    data = {'number': e}
    print(data)
    try:
        record_metadata = producer.send(topic_name,value=data).get(timeout=10)
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)
        sleep(0.5)
    except Exception as e:
        print(e)