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
    bluesky_client = BlueskyClient(username, password, "movie")

    request_limit = 3000  # Limit as per Bluesky API (3,000 requests per 5 minutes)
    request_window_duration = 5 * 60  # 5 minutes in seconds
    request_count = 0
    request_window_start = time.time()

    while True:
        current_time = time.time()
        # Reset request count if the current window has elapsed
        if current_time - request_window_start > request_window_duration:
            request_count = 0
            request_window_start = current_time

        # Check if request limit has been reached
        if request_count >= request_limit:
            sleep_time = request_window_duration - (current_time - request_window_start)
            print(f"Request limit reached. Sleeping for {sleep_time} seconds.")
            time.sleep(sleep_time)
            request_count = 0
            request_window_start = time.time()

        try:
            # Authenticate and fetch posts from Bluesky
            bluesky_client.authenticate()
            posts = bluesky_client.search_posts(limit=100)
            request_count += 1

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
                    time.sleep(0.05)
                except (TypeError, ValueError) as e:
                    print(f"Error serializing post to JSON: {e}\n{post}")
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(1)  # Short sleep to avoid hitting rate limits too quickly
