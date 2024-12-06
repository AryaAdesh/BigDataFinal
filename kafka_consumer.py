import json
from kafka import KafkaConsumer
import configparser
from mongo_client import MongoDBClient


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

        # MongoDB Client
        self.mongo_client = MongoDBClient(config_path)

    def consume_posts(self):
        print(f"Consuming messages from topic: {self.config['KAFKA']['topic']}")
        # Removed unnecessary poll method as it is not required for consuming messages
        try:
            print(f"Listening for messages...")
            for message in self.consumer:
                post_data = message.value
                # Insert received post data into MongoDB using MongoDBClient
                self.mongo_client.insert_tweet(post_data)
        except Exception as e:
            print(f"An error occurred while consuming messages: {e}")


if __name__ == "__main__":
    consumer_client = KafkaConsumerClient()
    consumer_client.consume_posts()