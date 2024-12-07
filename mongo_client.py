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

    def sync_historical_data(self, es_client):
        """
        Sync historical data from MongoDB to Elasticsearch.
        """
        try:
            print("Syncing historical data to Elasticsearch...")
            cursor = self.collection.find({})  # Fetch all documents from MongoDB

            for document in cursor:
                # Send to Elasticsearch
                es_client.upsert_elasticsearch(document)

            print("Historical data sync completed.")

        except Exception as e:
            print(f"Error syncing historical data: {e}")

    def watch_for_changes(self, es_client):
        """
        Watch for real-time changes in MongoDB and sync with Elasticsearch.
        """
        try:
            with self.collection.watch() as stream:
                print("Watching for real-time changes in MongoDB...")
                for change in stream:
                    if change["operationType"] in ["insert", "update"]:
                        # Fetch the full document after insert/update
                        updated_doc = self.collection.find_one({'_id': change['documentKey']['_id']})
                        if updated_doc:
                            # Send the document to Elasticsearch
                            es_client.upsert_elasticsearch(updated_doc)

                    elif change["operationType"] == "delete":
                        # Handle deletion if required
                        deleted_cid = change['documentKey']['_id']
                        es_client.delete_document(deleted_cid)

        except pymongo.errors.PyMongoError as e:
            print(f"Error listening to MongoDB changes: {e}")
