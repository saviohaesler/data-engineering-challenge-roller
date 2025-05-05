from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost')
for _ in range(5):
    future = producer.send('helloworld', b'some_message_bytes')
    result = future.get(timeout=60)
    print (result)
