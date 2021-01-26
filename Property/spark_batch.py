from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

"""
TO DO: put this up onto aws cluster
"""

property_schema = StructType(
   [
    StructField("borough", StringType(), True),
    StructField("numberbeds", IntegerType(), True),
    StructField("price", IntegerType(), True),
    StructField("url", StringType(), True)
   ]
)


spark = SparkSession.Builder()\
   .appName("PropertyAnalyse")\
   .getOrCreate()


property_df = spark\
   .read\
   .format("csv")\
   .schema(property_schema)\
   .option("header", "false")\
   .load("/Users/weilu/Scraper/*.csv")


average_price = property_df.groupBy("borough").avg("price")


print(average_price.show(50))







