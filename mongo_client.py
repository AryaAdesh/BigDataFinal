import configparser
import pymongo


class MongoDBClient:
    def __init__(self, config_path='config.ini'):
        # Read MongoDB configuration from config file
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # MongoDB Setup
        self.mongo_client = pymongo.MongoClient(self.config['MONGODB']['uri'])
        self.db = self.mongo_client[self.config['MONGODB']['database']]
        self.collection = self.db[self.config['MONGODB']['collection']]

        # Create a unique index on 'cid' to ensure no duplicate tweets are stored
        self.collection.create_index([("cid", pymongo.ASCENDING)], unique=True)

    def insert_tweet(self, tweet):
        self.collection.update_one(
            {'cid': tweet['cid']},
            {'$set': tweet},
            upsert=True
        )
        print(f"Upserted tweet with cid: {tweet['cid']}")
        print(f"Inserted tweet with cid: {tweet['cid']}")