# Single Node Kafka Cluster on AWS EC2

1. Go to AWS website and login to your account 
2. Click 'EC2' (Elastic Cloud Computing) service icon 
3. Click Launch Instance, and select Free Tier eligable options. Also you should create ( or customize) security groups to allow SSH and TCP from anywhere
4. Click Launch Instance and wait until your instance state is 'Running'
5. Copy your public IPv4 address and use Putty (or some similar software) to login into your AWS Linux instance
6. Once you have logged in follow this steps  to set up Kafka on your EC2 instance:
7. Download Apache Kafka to your instance with following command:

        wget https://downloads.apache.org/kafka/3.6.0/kafka_2.12-3.6.0.tgz
8. Unpack zip file with:
        tar -xvf kafka_2.12-3.6.0.tgz

9. Install java:

        sudo jum install java
10. Check for java version
        
        java -version
        cd kafka_2.12-3.6.0
            
11. Start zookeeper with:
                
        bin/zookeeper-server-start.sh config/zookeeper.properties
            
12. Open one more session ( basically open new terminal)

13. Limit Kafka Heap Volume by writting this line to terminal to limit memory usage by kafka. :

        export KAFKA_HEAP_OPTS='-Xmx256M -Xms128M'
        
    without this line Kafka would take up whole amount of space of our instance ( which is in our free tier instance not much)

14. Start kafka broker (server):

                
        bin/kafka-server-start.sh config/server.properties

    Problem with this configuration is that ip address of server is pointing to private IPv4 address of your EC2 instance and as such is unreachable from outside of instance (for example for user/client from the web because it can not detect this private IP). We need to change server.properties in our config folder --> change (or add) adverse.listener equal to public ip address of your instance .

15. After making changes to server.properties start kafka server (broker) once again with:

                
        bin/kafka-server-start.sh config/server.properties

16. Open one more session ( basically open new terminal) and create topic :
                
        bin/kafka-topics.sh --create --topic demo_test --bootstrap-server [your-server-public-IPv4:9092] --replication-factor 1 --partitions 1

17. After topic is created we can start producer and consumer (in separate terminals):

        bin/kafka-console-producer.sh --topic demo_test --bootstrap-server [your-server-public-IPv4:9092]

        bin/kafka-console-consumer.sh --topic demo_test --bootstrap-server [your-server-public-IPv4:9092] --partition 0

18. Now you can start writing messages to producer console and see those messages on consumer console.



