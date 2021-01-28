from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType


def processor(spark, input_data, output_data):

    property_schema = StructType(
        [
            StructField("borough", StringType(), True),
            StructField("numberbeds", IntegerType(), True),
            StructField("price", IntegerType(), True),
            StructField("url", StringType(), True)
        ]
    )

    property_df = spark.read.format("csv").schema(property_schema).option("header", "false").load(input_data)

    average_price = property_df.groupBy("borough", 'numberbeds').avg("price").orderBy('borough', 'numberbeds', ascending=True)

    # print(average_price.show(10))

    average_price.repartition(1).write.option("header", "true").csv(output_data)


def create_spark_session():
    spark = SparkSession.Builder() \
        .appName("PropertyAnalyse") \
        .getOrCreate()
    return spark


def main():
    ss = create_spark_session()
    input_data = 's3n://property-prices-borough/input/data/*.csv'
    output_data = 's3n://property-prices-borough/output/data/'

    processor(ss, input_data, output_data)


if __name__ == "__main__":
    main()

