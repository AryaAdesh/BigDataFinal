import json
from kafka import KafkaConsumer
import configparser
import pymongo

# Kafka Consumer Setup
class KafkaConsumerClient:
    def __init__(self, config_path='config.ini'):
        # Read Kafka configuration from config file
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        self.consumer = KafkaConsumer(
            self.config['KAFKA']['topic'],
            bootstrap_servers=self.config['KAFKA']['bootstrap_servers'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='twitter_data_consumer_group',
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )

        # MongoDB Setup
        self.mongo_client = pymongo.MongoClient(self.config['MONGODB']['uri'])
        self.db = self.mongo_client[self.config['MONGODB']['database']]
        self.collection = self.db[self.config['MONGODB']['collection']]

    def consume_posts(self):
        print(f"Consuming messages from topic: {self.config['KAFKA']['topic']}")
        # Removed unnecessary poll method as it is not required for consuming messages
        try:
            print(f"Listening for messages...")
            for message in self.consumer:
                post_data = message.value
                # Insert received post data into MongoDB
                self.collection.insert_one(post_data)
                print(f"Inserted post into MongoDB with CID: {post_data.get('cid')}")
        except Exception as e:
            print(f"An error occurred while consuming messages: {e}")

# Example Usage
if __name__ == "__main__":
    consumer_client = KafkaConsumerClient()
    consumer_client.consume_posts()
