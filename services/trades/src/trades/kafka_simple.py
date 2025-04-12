"""
A simple file that uses quixstreams to produce data which would be sent to kafka topic
"""


from quixstreams import Application
import time
import random

# Initialize the app
app = Application(broker_address="172.20.0.2:31092",
                  consumer_group="example")  

# Create a topic and producer
topic = app.topic(name="dummy-topic", value_serializer="json")
producer = app.get_producer()


# Simulate sending dummy dicts
with producer:
    for i in range(10):  # Send 10 dummy messages
        dummy_data = {
            "id": str(i),
            "name": f"item_{i}",
            "value": random.randint(1, 100)
        }

        # Serialize the message using the topic
        message = topic.serialize(key=dummy_data['id'], value=dummy_data)

        producer.produce(topic=topic.name, 
                         value=message.value,
                         key=message.key)
        
        print(f"Produced: {dummy_data}")
        time.sleep(1)
