import time
import random
from unittest.util import three_way_cmp

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

    def search_posts(self, term, limit=100):
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
        data = response.json().get("posts", [])
        print([x['record']['text'] for x in data])
        return response.json().get("posts", [])

    def get_followers(self, target_username, limit = 1000):
        url = "https://bsky.social/xrpc/app.bsky.graph.getFollowers"
        headers = {
            "Authorization": f"Bearer {self.session_token}"
        }
        params = {
            "actor": target_username
        }

        followers = []
        cursor = None

        while len(followers) < limit:
            if cursor:
                params["cursor"] = cursor

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            resp_json = response.json()
            followers.extend(
                [
                    {'did': d['did'], 'handle': d['handle']} for d in resp_json['followers']
                ]
            )
            cursor = response.json().get("cursor", None)
        return followers


    def get_user_posts(self, target_username):
        url = "https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed"
        headers = {
            "Authorization": f"Bearer {self.session_token}"
        }
        params = {
            "actor": target_username
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get user threads: {response.json()}")

    def fetch_multiple_users_threads(self, user_ids, threads_per_user=100):
        headers = {
            "Authorization": f"Bearer {self.session_token}"
        }

        all_user_threads = {}

        for user_id in user_ids:
            user_threads = []
            cursor = None

            while len(user_threads) < threads_per_user:
                params = {
                    "actor": user_id
                }
                if cursor:
                    params["cursor"] = cursor

                response = requests.get(f"{self.base_url}app.bsky.feed.getAuthorFeed",
                                        headers=headers,
                                        params=params)


                if response.status_code != 200:
                    print(f"Error fetching threads for user {user_id}: {response.status_code}, {response.text}")
                    break

                data = response.json()
                feed = data.get("feed", [])
                new_threads = []
                for th in feed:
                    text = th['post']['record']['text']
                    if len(text) > 50:
                        processed_thread = {'cid': th['post']['cid'], 'lang': th['post']['record'].get('langs', []),
                                            'text': text, 'createdAt': th['post']['record']['createdAt']}

                        new_threads.append(processed_thread)

                user_threads.extend(new_threads)

                cursor = data.get("cursor")
                if not cursor:
                    break

                time.sleep(0.5)  # Add a small delay to avoid rate limiting

            all_user_threads[user_id] = user_threads

        return all_user_threads