import pyspark.sql.types as T
import pyspark.sql.functions as F

def data_clean(df):

    df = (
        df.withColumn(
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
    return df