import praw
import json
import requests
import os
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

def fetch_images(limit=10):
    subreddit = reddit.subreddit("greentext")
    images = []

    for post in subreddit.new(limit=limit):
        if post.is_self:
            continue
        
        image_url = post.url
        if image_url.endswith(("jpg", "jpeg", "png")): 
            images.append({
                "title": post.title,
                "upvotes": post.score,
                "url": post.url,
                "image_url": image_url
            })
    
    return images

def download_images(images, folder="images"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for i, item in enumerate(images):
        image_url = item["image_url"]
        filename = os.path.join(folder, f"{i+1}.jpg")

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
    images = fetch_images(limit=10)
    download_images(images)
