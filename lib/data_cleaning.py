from pyspark.sql.functions import col, when


class DataCleaner:
    def remove_bad_values(df):
        # Create a dictionary that maps columns to bad values
        bad_values = {
            "title": "No Title Data Available",
            "description": "No description available Story format",
            "follower_count": "User Info Error",
            "tag_list": "N,o, ,T,a,g,s, ,A,v,a,i,l,a,b,l,e",
            "image_src": "Image src error.",
        }

        # Iterate over the dictionary and replace the bad values with null
        for column, bad_value in bad_values.items():
            df1 = df1.withColumn(
                column, when(col(column) == bad_value, None).otherwise(col(column))
            )
