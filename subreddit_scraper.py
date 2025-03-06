import praw
import requests
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

def get_args():
    parser = argparse.ArgumentParser(description="Fetch images from a subreddit.")
    parser.add_argument("--subreddit", type=str, default="itookapicture", help="Subreddit to fetch from")
    parser.add_argument("--limit", type=int, default=10, help="Number of posts to fetch")
    return parser.parse_args()

def fetch_images(subreddit, limit):
    subreddit = reddit.subreddit(subreddit)
    images = []

    for post in subreddit.new(limit=limit):
        if not post.is_self and post.url.endswith(("jpg", "jpeg", "png", "gif")):
            images.append({
                "title": post.title,
                "upvotes": post.score,
                "url": post.url,
                "image_url": post.url
            })

    return images

def download_images(images, folder="images"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for i, item in enumerate(images):
        image_url = item["image_url"]
        filename = os.path.join(folder, f"image_{i+1}.jpg")

        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"✅ Downloaded: {filename}")
            else:
                print(f"Failed to download: {image_url}")
        except Exception as e:
            print(f"Error downloading {image_url}: {e}")

if __name__ == "__main__":
    args = get_args()
    print(f"🔍 Fetching {args.limit} posts from r/{args.subreddit}...")
    
    posts = fetch_images(args.subreddit, args.limit)
    download_images(posts)
