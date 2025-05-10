"""
A simple file that uses quixstreams to produce data which would be sent to kafka topic
"""


import random
import time

from quixstreams import Application

# Initialize the app
app = Application(broker_address="localhost:9092",
                  consumer_group="exmple2")

# Create a topic and producer
topic = app.topic(name="dummy-topic2", value_serializer="json")
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
