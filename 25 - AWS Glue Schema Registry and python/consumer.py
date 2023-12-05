import os
import boto3
from dotenv import load_dotenv

# In this example we will use kafka-python as our Kafka client,
# so we need to have the `kafka-python` extras installed and use
# the kafka adapter.
from aws_schema_registry import SchemaRegistryClient
from aws_schema_registry.adapter.kafka import KafkaDeserializer
from aws_schema_registry import DataAndSchema, SchemaRegistryClient
from kafka import KafkaConsumer

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

# Create the deserializer
deserializer = KafkaDeserializer(client)

# Create the consumer
consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'], value_deserializer=deserializer,auto_offset_reset ='earliest')
consumer.subscribe('aws_glue_schema')

# Now use the consumer normally
for message in consumer:
    # The deserializer produces DataAndSchema instances
    value: DataAndSchema = message.value
    # which are NamedTuples with a `data` and `schema` property
    value.data == value[0]
    value.schema == value[1]
    # and can be deconstructed
    data, schema = value
    
    print (value)