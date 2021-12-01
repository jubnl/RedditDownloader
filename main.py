from RedditDownloader import RedditBot
from utils import get_credentials, Scales

redditbot = RedditBot(get_credentials())
redditbot.save_images_from_subreddit(
    scale=Scales.YoutubeShortsFullscreen,
    replace_resized=False,
    amount=1
)
