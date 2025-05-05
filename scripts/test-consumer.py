from kafka import KafkaConsumer
from kafka import TopicPartition
consumer = KafkaConsumer('helloworld',bootstrap_servers='localhost')
for msg in consumer:
    print (msg)
