# Spark master URL
import os
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator




# Create a SparkConf


class SparkSession(object):

    spark_session = None
    spark_master = None
    conf = None

    def __init__(self, app_name: str):
        self.app_name = app_name
        if self.spark_session is None:
            self.start_spark()


    def start_spark(self):
        self.spark_master = os.environ['SPARK_MASTER']

        self.conf = SparkConf().setAppName(self.app_name).setMaster(self.spark_master)
        self.spark_session = SparkSession.builder \
            .appName("ElasticsearchKMeans") \
            .config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-30_2.12:7.17.0") \
            .getOrCreate()



    def load_df_from_es(self, es_read_conf, vector_field: str, output_col_name: str):
        spark = self.spark_session
        df = spark.read.format("org.elasticsearch.spark.sql").options(**es_read_conf).load()
        assembler = VectorAssembler(inputCols=[vector_field], outputCol=output_col_name)
        vector_df = assembler.transform(df)
        return vector_df



def k_means_clustering(k, vector_df, seed = 1):
    kmeans = KMeans(k=k, seed=seed)  # Adjust k as needed
    model = kmeans.fit(vector_df)

    predictions = model.transform(vector_df)

    evaluator = ClusteringEvaluator()
    silhouette = evaluator.evaluate(predictions)
    print(f"Silhouette with squared euclidean distance: {silhouette}")


    centers = model.clusterCenters()
    print("Cluster Centers: ")
    for center in centers:
        print(center)

    return predictions


def get_all_cluster_points(predictions, vector_field):
    # Get all cluster assignments
    cluster_assignments = predictions.select("prediction").collect()

    # Count the number of points in each cluster
    cluster_counts = predictions.groupBy("prediction").count().orderBy("prediction")
    cluster_counts.show()

    # Optional: Get detailed information about each point and its cluster
    detailed_results = predictions.select(vector_field, "prediction")
    detailed_results.show(truncate=False)


def run_k_means(vector_field='text', k=10, seed = 1):
    predictions = k_means_clustering(k, vector_field, seed)
    get_all_cluster_points(predictions, vector_field)
    return predictions

if __name__ == "__main__":
    vector_field = os.environ.get('KMeansVectorField')
    clusters = int(os.environ.get('KMeansClusters'))
    run_k_means(vector_field=vector_field, k=clusters)