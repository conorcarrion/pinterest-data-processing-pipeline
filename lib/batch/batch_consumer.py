import logging
import json
import uuid
from kafka import KafkaConsumer
from kafka import TopicPartition


class MyKafkaConsumer:
    def __init__(self, bootstrap_servers, topic):
        self.consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset="earliest",
            value_deserializer=lambda message: json.loads(message),
            consumer_timeout_ms=1000,
        )

        self.consumer.assign([TopicPartition("Pins", 0)])

    def consume_messages_to_bucket(self, bucket_client, bucket):
        for message in self.consumer:
            filename = str(uuid.uuid4())
            try:
                bucket_client.write_to_bucket(bucket, f"{filename}.json", message.value)
            except Exception as e:
                logging.error(e)
        self.consumer.close()

    def print_messages(self):
        for message in self.consumer:
            print(message.value)
