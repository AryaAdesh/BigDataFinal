import random
import requests
import configparser


class BlueskyClient:
    def __init__(self, username, password):
        self.base_url = "https://bsky.social/xrpc/"
        self.username = username
        self.password = password
        self.session_token = None

    def authenticate(self):
        url = f"{self.base_url}com.atproto.server.createSession"
        payload = {
            "identifier": self.username,
            "password": self.password
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        self.session_token = response.json().get("accessJwt")

    def search_posts(self, term="the", limit=100):
        if not self.session_token:
            raise ValueError("Client is not authenticated. Please call authenticate() first.")

        url = f"{self.base_url}app.bsky.feed.searchPosts"
        headers = {
            "Authorization": f"Bearer {self.session_token}"
        }
        params = {
            "q": term,
            "limit": limit
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("posts", [])


config = configparser.ConfigParser()
config.read('config.ini')

username = config['CREDENTIALS']['username']
password = config['CREDENTIALS']['password']

client = BlueskyClient(username, password)
try:
    client.authenticate()
    posts = client.search_posts(limit=100)
    print("Posts:")
    import json
    for post in posts:
        try:
            print(json.dumps(post, indent=2))
        except (TypeError, ValueError) as e:
            print(f"Error serializing post to JSON: {e}{post}")

except Exception as e:
    print(f"An error occurred: {e}")
