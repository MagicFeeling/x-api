#!/usr/bin/env python3
"""
X (Twitter) Image Poster
Posts images to X using OAuth 1.0a authentication
"""

import json
import os
import sys
from pathlib import Path
import tweepy


def load_config(config_path='config.json'):
    """Load configuration from JSON file and expand project_folder"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Expand project_folder path if it exists
        if "project_folder" in config:
            project_folder = Path(config["project_folder"]).expanduser()
            config["project_folder"] = str(project_folder)

        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        sys.exit(1)


def load_caption(caption_file_path, project_folder=None):
    """Load caption text from file"""
    try:
        # Build full path if project_folder exists
        if project_folder and not os.path.isabs(caption_file_path):
            caption_file_path = os.path.join(project_folder, caption_file_path)

        with open(caption_file_path, 'r', encoding='utf-8') as f:
            caption = f.read().strip()

        return caption
    except FileNotFoundError:
        print(f"Warning: Caption file '{caption_file_path}' not found. Using empty caption.")
        return ""
    except Exception as e:
        print(f"Warning: Error reading caption file: {e}. Using empty caption.")
        return ""


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


def post_tweet(config, tweet_text, image_paths=None, video_path=None):
    """Post a tweet with optional images (up to 4) or a video"""
    try:
        # Create client and API
        client = create_client(config)
        api = create_api(config)

        media_ids = []

        # Upload video if provided (mutually exclusive with images)
        if video_path:
            if os.path.exists(video_path):
                print(f"Uploading video: {video_path}")
                media = api.media_upload(filename=video_path, media_category='tweet_video')
                media_ids.append(media.media_id)
                print(f"Video uploaded successfully. Media ID: {media.media_id}")
            else:
                print(f"Warning: Video not found: {video_path}")
        # Upload images if provided (only if no video)
        elif image_paths:
            for image_path in image_paths:
                if os.path.exists(image_path):
                    print(f"Uploading image: {image_path}")
                    media = api.media_upload(filename=image_path)
                    media_ids.append(media.media_id)
                    print(f"Image uploaded successfully. Media ID: {media.media_id}")
                else:
                    print(f"Warning: Image not found: {image_path}")

        # Post tweet
        print(f"Posting tweet ({len(tweet_text)} chars): {tweet_text[:100]}...")
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


def main():
    """Main function"""
    print("=" * 50)
    print("X (Twitter) Image/Video Poster")
    print("=" * 50)

    # Load configuration
    config = load_config()

    # Get project folder
    project_folder = config.get('project_folder')

    # Check if video mode is enabled
    video_config = config.get('video', {})
    video_enabled = video_config.get('enabled', False)
    video_path = None

    if video_enabled:
        # Load video caption
        video_caption_file = video_config.get('caption_file', 'Prompts/video-preview.txt')
        caption = load_caption(video_caption_file, project_folder)

        # Get video file path
        video_file = video_config.get('file', 'Video/preview.mp4')
        if project_folder and not os.path.isabs(video_file):
            video_path = os.path.join(project_folder, video_file)
        else:
            video_path = video_file

        print(f"\nMode: VIDEO")
        print(f"Video file: {video_path}")
        exists = "✓" if os.path.exists(video_path) else "✗"
        print(f"  {exists} {os.path.basename(video_path)}")

        if caption:
            print(f"Caption loaded: {len(caption)} characters")
        else:
            print("Warning: No caption loaded")
            caption = ""
    else:
        # Load caption from config
        caption_file = config.get('caption', {}).get('file', '')
        if caption_file:
            caption = load_caption(caption_file, project_folder)
            if caption:
                print(f"\nCaption loaded: {len(caption)} characters")
            else:
                print("\nWarning: No caption loaded")
                caption = ""
        else:
            caption = ""

        # Get image paths from config
        image_paths = []
        media = config.get('media', {})

        # Check for SFW file
        if 'sfw_file' in media and media['sfw_file']:
            sfw_file = media['sfw_file']
            # Build full path if project_folder exists and path is relative
            if project_folder and not os.path.isabs(sfw_file):
                sfw_file = os.path.join(project_folder, sfw_file)
            image_paths.append(sfw_file)

        # Check for NSFW file
        if 'nsfw_file' in media and media['nsfw_file']:
            nsfw_file = media['nsfw_file']
            # Build full path if project_folder exists and path is relative
            if project_folder and not os.path.isabs(nsfw_file):
                nsfw_file = os.path.join(project_folder, nsfw_file)
            image_paths.append(nsfw_file)

        # Display images to post
        print(f"\nMode: IMAGES")
        print(f"Images to post: {len(image_paths)}")
        for path in image_paths:
            exists = "✓" if os.path.exists(path) else "✗"
            print(f"  {exists} {os.path.basename(path)}")

        if not image_paths:
            print("\nWarning: No images specified in config")

    print("\nPosting to X...")
    print("-" * 50)

    # Post tweet
    if video_enabled:
        post_tweet(config, caption, video_path=video_path)
    else:
        post_tweet(config, caption, image_paths=image_paths if image_paths else None)

    print("-" * 50)
    print("\n✓ All done!")


if __name__ == "__main__":
    main()
