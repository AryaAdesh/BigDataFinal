from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Kafka setup
consumer = KafkaConsumer(
    'twitter_data_topic',
    bootstrap_servers='localhost:9092',  # Adjust this if needed
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# MongoDB setup
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["twitter_db"]
mongo_collection = mongo_db["tweets"]

# Consume messages from Kafka and store in MongoDB
for message in consumer:
    mongo_collection.insert_one(message.value)
    print(f"Inserted into MongoDB: {message.value}")
