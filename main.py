from RedditDownloader import RedditBot
from utils import SocialMedias, get_credentials, Scales

reddit = RedditBot(get_credentials())
data = reddit.save_images_from_subreddit(
    amount=5,
    subreddits=("dankmemes",),
    scale=Scales.InstagramPhotoSquare
)
video_path = reddit.create_video(data)

ytb_data = {
    "file": video_path,
    "title": "#short \n Memes but this time you laugh for real",
    "description": "why tho",
    "keywords": "meme,memes,laugh,internet,short",
    "privacyStatus": "public"
}

reddit.publish_on(SocialMedias.YouTube, ytb_data)
