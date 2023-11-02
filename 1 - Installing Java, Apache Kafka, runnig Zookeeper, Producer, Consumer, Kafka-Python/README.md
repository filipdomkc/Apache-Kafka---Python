# Setting up Apache Kafka on Windows

This guide will walk you through the process of installing Java, Apache Kafka, and running your first ZooKeeper, Kafka server, producer, and consumer on a Windows system from the command line.

## Installing Java

1. Download the latest version of Java Development Kit (JDK) for Windows from the [Oracle website](https://www.oracle.com/java/technologies/javase-downloads.html).

2. Run the installer and follow the installation instructions.

3. After installation, open your Windows Command Prompt and check the Java version to ensure it's properly installed by running:
   ```bash
   java -version

## Installing Apache Kafka

1. Download the latest Apache Kafka release for Windows from the Apache Kafka website.

2. Extract the Kafka archive to a directory of your choice. For example, you can use a tool like 7-Zip or simply right-click the archive and select "Extract All."

## Running ZooKeeper

1. Open a Windows Command Prompt and navigate to your Kafka directory where you extracted the Kafka archive.

2. Start ZooKeeper by running the following command:
    ```bash
    bin\windows\zookeeper-server-start.bat config\zookeeper.properties

## Running Kafka Server

1. Open a new Command Prompt window (leave the ZooKeeper window open), and navigate to the Kafka directory.

2. Start the Kafka server by running the following command:
    ```bash
    bin\windows\kafka-server-start.bat config\server.properties

## Running Kafka Producer

1. Open another Command Prompt window (leave the ZooKeeper and Kafka server windows open), and navigate to the Kafka directory.

2. Create a Kafka topic and then produce messages to it. Replace your-topic with the name of your topic and provide a message. For example:
    ```bash
    bin\windows\kafka-topics.bat --create --topic your-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

    bin\windows\kafka-console-producer.bat --topic your-topic --bootstrap-server localhost:9092

## Running Kafka Consumer

1. Open a final Command Prompt window (leave the ZooKeeper, Kafka server, and producer windows open), and navigate to the Kafka directory.

2. Consume messages from the Kafka topic you created earlier. Replace your-topic with your topic name.
    ```bash
    bin\windows\kafka-console-consumer.bat --topic your-topic --bootstrap-server localhost:9092 --from-beginning

You should now have Java, Apache Kafka, and ZooKeeper up and running on your Windows system, with a producer and consumer actively sending and receiving messages. You can interact with these components to explore the capabilities of Apache Kafka.

# kafka-python

To use kafka-python as a producer to send messages to your Kafka topic and have the consumer from the previous steps see those messages, you can follow these instructions:

1. Create virtual environment and activate it.

2. Make sure you have the kafka-python library installed. You can install it using pip:
    ```bash
    pip install kafka-python

3. In your Kafka setup, make sure you have already created the Kafka topic you intend to use. You can use the kafka-topics command as shown in the previous instructions to create the topic, or you can create it programmatically with kafka-python if it doesn't exist yet.

4. Save your producer script to a file, for example, kafka_producer.py.

5. Modify your script to ensure the producer uses the topic you want to send messages to. Replace "your-topic-name" with your desired topic name.
    ```python
    from time import sleep
    from json import dumps
    from kafka import KafkaProducer

    topic_name = "your-topic-name"  # Replace with your desired topic name

    producer = KafkaProducer(bootstrap_servers=["localhost:9092"], value_serializer=lambda x: dumps(x).encode('utf-8'))

    for e in range(1000):
        data = {'number': e}
        print(data)
        producer.send(topic_name, value=data)
        sleep(5)

6. Now, you can run your producer script by executing it in your terminal:
    ```bash
    python kafka_producer.py

This will start sending messages to your specified Kafka topic. The consumer you set up earlier should be able to consume these messages from the same topic.

Ensure that your Kafka server and ZooKeeper are still running, and that your Kafka server is listening on localhost:9092 as specified in the producer script. The consumer should be set to consume from the same topic, so it can receive the messages you're producing.
