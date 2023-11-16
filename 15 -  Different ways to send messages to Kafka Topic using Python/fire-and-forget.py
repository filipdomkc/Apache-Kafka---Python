#Fire-and-forget

from time import sleep
from json import dumps
from kafka import KafkaProducer

topic_name = 'fire-and-forget'
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer = lambda x: dumps(x).encode('utf-8'))

for e in range (100):
    data = {'number': e}
    print(data)
    producer.send(topic_name,value=data)
    sleep(0.5)