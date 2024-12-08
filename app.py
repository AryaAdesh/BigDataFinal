from mongo_client import MongoDBClient
from elastic_search_client import ElasticsearchClient


# Initialize MongoDB and Elasticsearch clients
mongo_client = MongoDBClient()
es_client = ElasticsearchClient()

# Step 1: Sync historical data
mongo_client.sync_historical_data(es_client)

# Step 2: Watch for real-time changes
mongo_client.watch_for_changes(es_client)