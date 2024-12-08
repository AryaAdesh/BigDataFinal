import configparser
import re
from datetime import datetime
import numpy as np
from elasticsearch import Elasticsearch
import spacy
import torch

nlp = spacy.load("en_core_web_lg")


def generate_embedding(text):
    """
    Generate a dense vector representation of the given text using SpaCy.
    Handles texts longer than SpaCy's max limit by splitting into chunks.
    """
    try:
        if not text or not isinstance(text, str) or not text.strip():
            raise ValueError("Text is empty or invalid")

        # Preprocess text
        text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)  # Remove unsupported characters
        text = text.strip()

        # Split text into chunks (SpaCy handles approximately 100,000 characters per document)
        max_chunk_size = 5000
        chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]

        # Generate embeddings for each chunk
        embeddings = []
        for chunk in chunks:
            print(f"Generating embedding for chunk: {chunk[:50]}...")  # Log first 50 characters
            doc = nlp(chunk)  # Process text with SpaCy
            embeddings.append(doc.vector)  # Get document-level vector

        # Combine chunk embeddings by averaging
        final_embedding = np.mean(embeddings, axis=0)
        return final_embedding

    except Exception as e:
        print(f"Error generating embedding for text: {text}. Error: {e}")
        return None



class ElasticsearchClient:
    def __init__(self, config_path='config.ini'):
        # Read Elasticsearch configuration from config file
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # Elasticsearch Setup
        self.es = Elasticsearch([self.config['ELASTICSEARCH']['host']])
        self.index_name = self.config['ELASTICSEARCH']['index_name']
        self.setup_elasticsearch_index()

    def setup_elasticsearch_index(self):
        # Create an index in Elasticsearch if it doesn't exist
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(
                index=self.index_name,
                body={
                    "mappings": {
                        "properties": {
                            "vector": {
                                "type": "dense_vector",
                                "dims": int(self.config['ELASTICSEARCH']['dimension'])
                            },
                            "text": {
                                "type": "text"
                            },
                            "created_at": {
                                "type": "date"
                            }
                        }
                    }
                }
            )
            print(f"Created Elasticsearch index: {self.index_name}")
        else:
            print(f"Using existing Elasticsearch index: {self.index_name}")

    def upsert_elasticsearch(self, tweet):
        """
        Upserts a tweet into Elasticsearch with text, embedding, and created_at fields.
        """
        text = tweet.get('text', '').strip()
        created_at = tweet.get('createdAt', '')


        # Validate and format created_at
        try:
            created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00")).isoformat() if created_at else None
        except ValueError:
            print(f"Invalid date format for created_at: {created_at}")
            created_at = None

        # Skip if text is empty
        if not text:
            print(f"Skipping tweet with cid: {tweet['cid']} due to empty or invalid text.")
            return

        # Generate vector embedding using SpaCy
        vector = generate_embedding(text)
        if vector is None:
            print(f"Skipping tweet with cid: {tweet['cid']} due to failed embedding generation. Text: {text}")
            return

        # Validate the vector
        if not isinstance(vector, (list, np.ndarray)) or len(vector) != 300:
            print(f"Invalid vector format for cid: {tweet['cid']}. Vector: {vector}")
            return

        # Index the document in Elasticsearch
        try:
            payload = {
                "vector": vector.tolist(),  # Convert to list if numpy array
                "text": text,
                "created_at": created_at
            }
            print(f"Indexing payload: {payload}")  # Log the payload
            self.es.index(
                index=self.index_name,
                id=tweet['cid'],
                body=payload
            )
            print(f"Upserted tweet in Elasticsearch with cid: {tweet['cid']}")
        except Exception as e:
            print(f"Error indexing document with cid: {tweet['cid']}. Error: {e}")

