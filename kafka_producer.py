import json
import time

from kafka import KafkaProducer
import configparser
from bluesky_api import BlueskyClient


# Kafka Producer Setup
class KafkaProducerClient:
    def __init__(self, config_path='config.ini'):
        # Read Kafka configuration from config file
        config = configparser.ConfigParser()
        config.read(config_path)

        self.producer = KafkaProducer(
            bootstrap_servers=config['KAFKA']['bootstrap_servers'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = config['KAFKA']['topic']

    def produce_post(self, post_data):
        try:
            self.producer.send(self.topic, value=post_data)
            print(f"Successfully produced post to topic {self.topic}: {json.dumps(post_data, indent=2)}")
        except Exception as e:
            print(f"Failed to produce post to Kafka: {e}")


if __name__ == "__main__":
    # Initialize Kafka producer client
    producer_client = KafkaProducerClient()

    # Initialize Bluesky client
    config = configparser.ConfigParser()
    config.read('config.ini')
    username = config['CREDENTIALS']['username']
    password = config['CREDENTIALS']['password']
    bluesky_client = BlueskyClient(username, password)

    try:
        # Authenticate and fetch posts from Bluesky
        bluesky_client.authenticate()
        posts = bluesky_client.search_posts(limit=100)

        # Produce each post to Kafka
        for post in posts:
            try:
                # Extract required fields
                cid = post.get("cid")
                display_name = post.get("author", {}).get("displayName")
                created_at = post.get("record", {}).get("createdAt")
                lang = post.get("record", {}).get("langs", [None])[0]
                text = post.get("record", {}).get("text")

                # Create a dictionary with the extracted data
                post_data = {
                    "cid": cid,
                    "displayName": display_name,
                    "createdAt": created_at,
                    "lang": lang,
                    "text": text
                }

                # Produce to Kafka topic
                producer_client.produce_post(post_data)
                time.sleep(1)
            except (TypeError, ValueError) as e:
                print(f"Error serializing post to JSON: {e}\n{post}")
    except Exception as e:
        print(f"An error occurred: {e}")
