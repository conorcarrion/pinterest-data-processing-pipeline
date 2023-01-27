import os
import pyspark.sql.types as T
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1,org.postgresql:postgresql:42.2.14 pyspark-shell"


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
    exploding_df.withColumn(
        "follower_count", F.regexp_replace("follower_count", "k", "000")
    )
    .withColumn("follower_count", F.regexp_replace("follower_count", "M", "000000"))
    .withColumn("save_location", F.regexp_replace("save_location", "Local save in", ""))
    .withColumn("follower_count", F.col("follower_count").cast("int"))
    .withColumn(
        "tag_list",
        F.regexp_replace(
            "tag_list", "N,o, ,T,a,g,s, ,A,v,a,i,l,a,b,l,e", "No Tags Available"
        ),
    )
    .filter(
        ~(
            (F.col("title") == "No Title Data Available")
            & (F.col("description") == "No description available Story format")
        )
    )
    .withColumn(
        "been_downloaded", F.when(F.col("downloaded") == 1, True).otherwise(False)
    )
    .drop("downloaded")
    .withColumnRenamed("been_downloaded", "downloaded")
    .drop("poster_name")
)


def write_to_postgres(df, epoch_id):
    df.write.format("jdbc").options(
        url="jdbc:postgresql://localhost:5432/pinterest_streaming",
        driver="org.postgresql.Driver",
        dbtable="experimental_data",
        user="postgres",
        password="pgpassword",
    ).mode("append").save()


# exploding_df.writeStream.outputMode("append").format(
#     "console"
# ).start().awaitTermination()

exploding_df.writeStream.outputMode("append").format("console").foreachBatch(
    write_to_postgres
).start().awaitTermination()
