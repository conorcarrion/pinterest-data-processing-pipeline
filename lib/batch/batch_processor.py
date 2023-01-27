from gcp_bucket import GCPBucketClient
from data_cleaning import DataCleaner
from batch_consumer import MyKafkaConsumer
from lib.batch_spark import BatchSpark


def run():
    client = GCPBucketClient()
    MyKafkaConsumer.consume_messages_to_bucket(client, "project-pin-api")
    spark = BatchSpark()
    df = spark.load_batch_from_bucket()
    df = DataCleaner.remove_bad_values(df)
    # load dataframe to HBASE or storage
    client.delete_json_files("project-pin-api")
