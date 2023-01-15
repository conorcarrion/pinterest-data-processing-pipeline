from kafka import KafkaConsumer
import json


class MyKafkaConsumer:
    def __init__(self, bootstrap_servers, topic):
        self.consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset="earliest",
            value_deserializer=lambda message: json.loads(message),
        )
        self.consumer.subscribe([topic])

    def read_messages(self):
        for message in self.consumer:
            print(message.value)
            print("consumer.close inside the loop")
            self.consumer.close()

    def upload_to_gcp_bucket(self):
        pass
