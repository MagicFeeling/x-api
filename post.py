#!/usr/bin/env python3
import json
import os
import sys
import tweepy

def load_config():
    """Load credentials from config.json"""
    with open('config.json', 'r') as f:
        return json.load(f)

def create_client(config):
    """Create and return authenticated Tweepy client"""
    client = tweepy.Client(
        consumer_key=config['api_key'],
        consumer_secret=config['api_key_secret'],
        access_token=config['access_token'],
        access_token_secret=config['access_token_secret']
    )
    return client

def create_api(config):
    """Create OAuth 1.0a API for media upload"""
    auth = tweepy.OAuth1UserHandler(
        config['api_key'],
        config['api_key_secret'],
        config['access_token'],
        config['access_token_secret']
    )
    return tweepy.API(auth)

def post_tweet(tweet_text, image_path=None):
    """Post a tweet with optional image"""
    try:
        # Load config
        config = load_config()

        # Create client and API
        client = create_client(config)
        api = create_api(config)

        media_ids = []

        # Upload image if provided
        if image_path and os.path.exists(image_path):
            print(f"Uploading image: {image_path}")
            media = api.media_upload(filename=image_path)
            media_ids.append(media.media_id)
            print(f"Image uploaded successfully. Media ID: {media.media_id}")

        # Post tweet
        print(f"Posting tweet: {tweet_text}")
        response = client.create_tweet(
            text=tweet_text,
            media_ids=media_ids if media_ids else None
        )

        tweet_id = response.data['id']
        print(f"✓ Tweet posted successfully!")
        print(f"Tweet ID: {tweet_id}")
        print(f"URL: https://x.com/user/status/{tweet_id}")

        return tweet_id

    except Exception as e:
        print(f"✗ Error posting tweet: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Get tweet text and image path from environment variables
    tweet_text = os.getenv('TWEET_TEXT', 'Hello from X API!')
    image_path = os.getenv('IMAGE_PATH', '')

    if not tweet_text:
        print("Error: TWEET_TEXT environment variable is required")
        sys.exit(1)

    post_tweet(tweet_text, image_path if image_path else None)
