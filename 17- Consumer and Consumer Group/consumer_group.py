from json import dumps
from kafka import KafkaProducer

topic_name = 'consumer_group'
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer = lambda x: dumps(x).encode('utf-8'))

while True:
    message = input ("Enter the message you want to sent : ")
    partition_no = int (input("In which partition you want to send? "))
    producer.send(topic_name, value = message, partition = partition_no)

producer.close()