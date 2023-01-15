from kafka import KafkaProducer
import json


class MyKafkaProducer:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda message: json.dumps(message).encode("ascii"),
        )

    def send_message(self, topic, **kwargs):
        self.producer.send(topic, **kwargs)
        self.producer.flush()
