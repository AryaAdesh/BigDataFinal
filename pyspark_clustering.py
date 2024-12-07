from elasticsearch import Elasticsearch
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.ml.linalg import Vectors
from pyspark.sql.types import ArrayType, DoubleType, StructType, StructField

# Step 1: Retrieve Data from Elasticsearch
def fetch_data_from_elasticsearch():
    es = Elasticsearch("http://localhost:9200")  # Replace with your cluster details
    index_name = "your-index"

    response = es.search(index=index_name, body={
        "_source": ["embedding"],  # Adjust based on your field names
        "size": 10000
    })

    data = [hit["_source"]["embedding"] for hit in response["hits"]["hits"]]
    return data

# Step 2: Convert to PySpark DataFrame
def create_pyspark_df(data):
    schema = StructType([StructField("embedding", ArrayType(DoubleType()), True)])
    data_with_schema = [(row,) for row in data]
    return spark.createDataFrame(data_with_schema, schema)

# Step 3: Prepare Data for Clustering
def prepare_features(df):
    # Convert the 'embedding' column from ArrayType to DenseVector
    df_with_vectors = df.rdd.map(lambda row: (Vectors.dense(row[0]),)).toDF(["embedding"])
    assembler = VectorAssembler(inputCols=["embedding"], outputCol="features")
    return assembler.transform(df_with_vectors)

# Step 4: Perform Clustering
def perform_clustering(df):
    kmeans = KMeans(k=5, seed=1, featuresCol="features", predictionCol="cluster")
    model = kmeans.fit(df)
    result = model.transform(df)
    return result

# Main Workflow
if __name__ == "__main__":
    spark = SparkSession.builder \
        .master("local") \
        .appName("PySpark Clustering Test") \
        .config("spark.hadoop.security.authentication", "false") \
        .config("spark.yarn.token.service.enabled", "false") \
        .getOrCreate()
    try:
        # Fetch data
        data = fetch_data_from_elasticsearch()

        # Convert to PySpark DataFrame
        pyspark_df = create_pyspark_df(data)

        # Prepare features for clustering
        feature_df = prepare_features(pyspark_df)

        # Perform clustering
        clustered_df = perform_clustering(feature_df)

        # Show results
        clustered_df.select("embedding", "cluster").show()
    finally:
        # Stop the Spark session
        if spark is not None:
            spark.stop()
