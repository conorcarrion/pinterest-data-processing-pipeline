import yaml
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext


class BatchSpark:
    def __init__(self):

        with open("config/spark.yaml", "r") as outfile:
            # Load the contents of the file as a dictionary
            self.credentials = yaml.safe_load(outfile)

        spark = (
            SparkSession.builder
            .appName("BatchSpark")
            .config("google.cloud.auth.service.account.enable", "true")
            .config("google.cloud.auth.service.account.json.keyfile", self.credentials["gcp_key_file"])
            .getOrCreate()
        )


        self.spark = spark
        return self.spark

    def load_batch_from_bucket(self):
        df = self.spark.read.json(self.credentials["gcp_bucket"])
        return df
