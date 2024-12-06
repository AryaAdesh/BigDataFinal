from kafka import KafkaProducer
import pandas as pd
import json
import time

# Load the CSV data
file_path = 'twitter_dataset.csv'
twitter_data = pd.read_csv(file_path)

# Kafka setup using kafka-python
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Adjust the broker address if needed
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

topic_name = 'twitter_data_topic'

# Iterate through the dataframe in chunks of 10 rows
batch_size = 10
for start in range(0, len(twitter_data), batch_size):
    # Get 10 rows at a time
    batch = twitter_data.iloc[start:start + batch_size]

    # Convert each row to a dictionary and send to Kafka
    for index, row in batch.iterrows():
        message = row.to_dict()
        producer.send(topic_name, value=message)
        print(f"Sent: {message}")

    # Add some delay between batches to simulate streaming data
    time.sleep(2)

# Ensure all messages are sent before closing
producer.flush()
producer.close()
