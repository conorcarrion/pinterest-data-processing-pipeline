import os
import yaml
import pyspark.sql.types as T
import pyspark.sql.functions as F
from admin.data_clean import data_clean
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1,org.postgresql:postgresql:42.2.14 pyspark-shell"


sc = SparkContext("local", "Kafka Stream")
ssc = StreamingContext(sc, 30)

spark = (
    SparkSession.builder
    .appName("Streaming")
    .getOrCreate()
)
data_stream = (
    spark.readStream.format("Kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "Pins")
    .option("startingOffsets", "earliest")
    .load()
)

data_string = data_stream.selectExpr("CAST(value as STRING)")


schema = T.ArrayType(
    T.StructType(
        [
            T.StructField("index", T.IntegerType()),
            T.StructField("unique_id", T.StringType()),
            T.StructField("title", T.StringType()),
            T.StructField("description", T.StringType()),
            T.StructField("poster_name", T.StringType()),
            T.StructField("follower_count", T.StringType()),
            T.StructField("tag_list", T.StringType()),
            T.StructField("is_image_or_video", T.StringType()),
            T.StructField("image_src", T.StringType()),
            T.StructField("downloaded", T.IntegerType()),
            T.StructField("save_location", T.StringType()),
            T.StructField("category", T.StringType()),
        ]
    )
)

df = data_string.withColumn(
    "temp", F.explode(F.from_json("value", schema))
).select("temp.*")


clean_df = data_clean(df)

with open("config/postgres.yaml", "r") as outfile:
    # Load the contents of the file as a dictionary
    credentials = yaml.safe_load(outfile)

def write_to_postgres(df):
    df.write.format("jdbc").options(
        url=credentials["url"],
        driver=credentials["driver"],
        dbtable=credentials["dbtable"],
        user=credentials["user"],
        password=credentials["password"],
    ).mode("append").save()

# print to console
# clean_df.writeStream.outputMode("append").format(
#     "console"
# ).start().awaitTermination()

# write to postgresql database
clean_df.writeStream.outputMode("append").format("console").foreachBatch(
    write_to_postgres
).start().awaitTermination()
