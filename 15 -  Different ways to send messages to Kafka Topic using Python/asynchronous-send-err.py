#Asynchronous send with error

from time import sleep
from json import dumps
from kafka import KafkaProducer

topic_name = 'asynchronous-send-err'
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer = lambda x: dumps(x).encode('utf-8'))

def on_send_success(record_metadata, message):
    print()
    print("""Successfully produced "{}" to topic {} and partition {} at offset {}""".format(message, record_metadata.topic,record_metadata.partition,record_metadata.offset))
    print()

def on_send_error(excp, message):
    print()
    print('Failed to write the message "{}", error: {}'.format(message, excp))

for e in range (100):
    data = {'number': e}
    record_metadata = producer.send(topic_name,value=data).add_callback(on_send_success, message=data).add_errback(on_send_error, message=data)
    print("Sent the message {} using send method".format(data))
    print()
    sleep(0.5) # we add sleep so we can manually terminate our broker, without that the process is too fast

producer.flush()
producer.close()