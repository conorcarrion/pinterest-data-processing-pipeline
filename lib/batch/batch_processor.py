from admin.gcp_bucket import GCPBucketClient
from admin.data_clean import data_clean
from batch_consumer import MyKafkaConsumer
from batch_spark import BatchSpark


def run():
    client = GCPBucketClient()
    MyKafkaConsumer.consume_messages_to_bucket(client, "project-pin-api")
    spark = BatchSpark()
    df = spark.load_batch_from_bucket()
    df = data_clean(df)
    # load dataframe to HBASE or storage
    client.delete_json_files("project-pin-api")
