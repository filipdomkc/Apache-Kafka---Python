import os
import boto3
from dotenv import load_dotenv


from aws_schema_registry.avro import AvroSchema

# In this example we will use kafka-python as our Kafka client,
# so we need to have the `kafka-python` extras installed and use
# the kafka adapter.
from aws_schema_registry.adapter.kafka import KafkaSerializer
from aws_schema_registry import DataAndSchema, SchemaRegistryClient
from kafka import KafkaProducer


# Load environment variables from .env file
load_dotenv()

# Access environment variables
access_key = os.getenv("AWS_ACCESS_KEY")
secret_key = os.getenv("AWS_SECRET_KEY")


# Pass your AWS credentials or profile information here
session = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name='us-east-1')

glue_client = session.client('glue')

# Create the schema registry client, which is a façade around the boto3 glue client
client = SchemaRegistryClient(glue_client, registry_name='my-demo-registry')

# Create the serializer
serializer = KafkaSerializer(client)

# Create the producer
producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'], value_serializer=serializer)

# Our producer needs a schema to send along with the data.
# In this example we're using Avro, so we'll load an .avsc file.
with open('user.avsc', 'r') as schema_file:
    schema = AvroSchema(schema_file.read())

# Send message data along with schema
data = {
    'name': 'John Doe',
    'age': 30 ,
    'height': 190
}
record_metadata=producer.send('aws_glue_schema', value=(data, schema)).get(timeout=10)
# the value MUST be a tuple when we're using the KafkaSerializer

print(record_metadata.topic)
print(record_metadata.partition)
print(record_metadata.offset)