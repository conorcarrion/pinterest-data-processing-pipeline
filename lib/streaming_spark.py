import os
import pyspark.sql.types as T
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1 pyspark-shell"

sc = SparkContext("local", "Kafka Consumer")
ssc = StreamingContext(sc, 30)

spark = SparkSession.builder.appName("Streaming").getOrCreate()

data_df = (
    spark.readStream.format("Kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "Pins")
    .option("startingOffsets", "earliest")
    .load()
)

data_df = data_df.selectExpr("CAST(value as STRING)")


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

exploding_df = data_df.withColumn(
    "temp", F.explode(F.from_json("value", schema))
).select("temp.*")


exploding_df = (
    exploding_df.withColumn("value", F.from_json(exploding_df["value"], schema))
    .select(F.col("value.*"))
    .drop("index")
    .withColumn("follower_count", F.regexp_replace("follower_count", "k", "000"))
    .withColumn("follower_count", F.regexp_replace("follower_count", "M", "000000"))
    .withColumn("save_location", F.regexp_replace("save_location", "Local save in", ""))
    .select(
        "title",
        "category",
        "description",
        "is_image_or_video",
        "save_location",
        "tag_list",
        "downloaded",
        "unique_id",
        "follower_count",
        "image_src",
    )
    .withColumn("follower_count", exploding_df["follower_count"].cast("int"))
)

exploding_df.writeStream.outputMode("append").format(
    "console"
).start().awaitTermination()
