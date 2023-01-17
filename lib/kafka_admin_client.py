from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.cluster import ClusterMetadata


class MyKafkaAdminClient:
    def __init__(self) -> None:

        self.admin_client = KafkaAdminClient(
            bootstrap_servers="localhost:9092", client_id="Kafka Administrator"
        )

    def create_topic(self, name):
        topic = [NewTopic(name, num_partitions=2, replication_factor=1)]
        self.admin_client.create_topics(topic)
        print(f"Topic called {name} created.")
