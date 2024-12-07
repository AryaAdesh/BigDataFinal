# Spark master URL
import os
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession


spark_master = "local[*]"

# Create a SparkConf
conf = SparkConf().setAppName("MySparkApp").setMaster(spark_master)

print(os.environ["SPARK_HOME"])
# Create a SparkSession
spark = SparkSession.builder \
    .config(conf=conf) \
    .appName("MySparkApp") \
    .getOrCreate()

# Get the SparkContext from SparkSession
sc = spark.sparkContext

print(f"Connected to Spark master: {sc.master}")

# Example operation using SparkContext
rdd = sc.parallelize([1, 2, 3, 4, 5])
sum_result = rdd.sum()
print(f"Sum using SparkContext: {sum_result}")

# Example operation using SparkSession
df = spark.createDataFrame([(1, "Alice"), (2, "Bob"), (3, "Charlie")], ["id", "name"])
df.show()

