from elasticsearch import Elasticsearch
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.ml.linalg import Vectors
from pyspark.sql.types import ArrayType, DoubleType, StructType, StructField, StringType
from datetime import datetime, timedelta

# Step 1: Retrieve Data from Elasticsearch
def fetch_data_from_elasticsearch():
    es = Elasticsearch("http://localhost:9200")  # Replace with your cluster details
    index_name = "tweet_vectors"

    current_time = datetime.utcnow()
    last_hour = current_time - timedelta(hours=2)
    start_time = last_hour.isoformat()
    end_time = current_time.isoformat()

    query = {
        "query": {
            "range": {
                "created_at": {
                    "gte": start_time,
                    "lt": end_time
                }
            }
        },
        "_source": ["vector", "text", "created_at"],  # Adjust based on your field names
        "size": 10000  # Adjust size as needed
    }

    response = es.search(index=index_name, body=query)

    data = [
        {
            "vector": hit["_source"]["vector"],
            "text": hit["_source"].get("text", ""),
            "created_at": hit["_source"].get("created_at", "")
        }
        for hit in response["hits"]["hits"]
    ]
    return data

# Step 2: Convert to PySpark DataFrame
def create_pyspark_df(data):
    schema = StructType([
        StructField("vector", ArrayType(DoubleType()), True),
        StructField("text", StringType(), True),
        StructField("created_at", StringType(), True)
    ])
    broadcast_data = spark.sparkContext.broadcast(data)
    data_with_schema = [(row['vector'], row['text'], row['created_at']) for row in broadcast_data.value]
    return spark.createDataFrame(data_with_schema, schema)

# Step 3: Prepare Data for Clustering
def prepare_features(df):
    # Convert the 'embedding' column from ArrayType to DenseVector
    df_with_vectors = df.rdd.map(lambda row: (Vectors.dense(row['vector']), row['text'], row['created_at'])) \
        .toDF(["embedding", "text", "created_at"])
    assembler = VectorAssembler(inputCols=["embedding"], outputCol="features")
    df_with_features = assembler.transform(df_with_vectors)
    return df_with_features.repartition(200)

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
        .config("spark.rpc.message.maxSize", "2047") \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()
    try:
        # Fetch data
        data = fetch_data_from_elasticsearch()

        if not data:
            print("No data found in the last 2 hours.")

        else:
            # Convert to PySpark DataFrame
            pyspark_df = create_pyspark_df(data)

            # Prepare features for clustering
            feature_df = prepare_features(pyspark_df)

            # Perform clustering
            clustered_df = perform_clustering(feature_df)

            # Show results
            clustered_df.show()
    finally:
        # Stop the Spark session
        if spark is not None:
            spark.stop()
