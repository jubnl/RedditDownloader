# Reddit Image Downloader

## Inspired by [ClarityCoders' AutoTube](https://github.com/ClarityCoders/AutoTube)

### Requirements

You need a reddit application for that. You can create one to the following link :https://www.reddit.com/prefs/apps

You can follow this tutorial to create your application : https://youtu.be/bMT9ZC9sBzI?t=228

### Installation steps
 1. Clone this repository
 2. open a console (bash, cmd, etc...) where you cloned the repo and enter the following command :

`pip install -r requirements.txt`

If it returns an error, try the following command :

`pip3 install -r requirements.txt`

Is it still doesn't work, make sure you that python and pip are properly installed.

 3. Rename the [.env_sample](.env_sample) file to .env
 4. Edit your .env file :
    - REDDIT_CLIENT_SECRET="YourClientSecret"
    - REDDIT_CLIENT_ID="YourClientId"
    - REDDIT_USER_AGENT="<AppName-AppVersion>"

A user agent for example : "<MemeAcquisition-v1.0>"

## How to use 

Some code will be more explicit :

````python
from RedditDownloader import RedditBot
from utils import get_credentials, Scales

redditbot = RedditBot(get_credentials())
redditbot.save_images_from_subreddit(
    scale=Scales.YoutubeShortsFullscreen,
    replace_resized=False,
    amount=1
)
````

## RedditBot

This class takes 2 arguments :
 - required : `env` - `environs.Env` instance that has been initialized. There's a utility function for that : 
`utils.get_credentials()`
 - optional : `log` - `True` to log to console operation, `False` by default

You then have a single method described below :

## RedditBot.save_images_from_subreddit()

All 6 keyword arguments are optional.

- `subreddits` - a tuple of strings that contains the subreddit names. By default, it will query the 
[memes](https://www.reddit.com/r/memes/) subreddit. Check out what's after the r/ to known what is the exact string
to add to the tuple.


- `amount` - how many images (posts) do you want to download (int). By default, 5.


- `filetypes` - A tuple that contains all the file extensions that you want to download. By default,
("jpg", "png", "gif"). It may be used to download only jps and png or only gif. It may raise errors with other file extensions.


- `nsfw` - bool. If set to True it will only download NSFW posts (marked NSFW by the community or mods).
If set to False it will only download SFW posts. By default, set to False.


- `scale` - tuple of ints. If passed, it will resize the downloaded images with the size passed as argument
(width, height). By default, None is passed so no resize occurs. Some sizes are already defined for TikTok, YouTube or Instagram. -> see [Scales](#scales)


- `replace_resized` - bool. Only works when a new scale is passed. If set to False the resized image will be placed in 
a "resized" folder along with the original images. If set to True it will replace the original images.


## Scales

There's some scales already defined. To access them, import `Scales` from `utils` :
````python
from utils import Scales
````

Scales for YouTube :
- Scales.YoutubeShortsFullscreen
- Scales.YoutubeShortsSquare
- Scales.YoutubeVideo

Scales for TikTok :
- Scales.TikTok


Scales for Instagram :
- Scales.InstagramPhotoSquare
- Scales.InstagramPhotoLandscape
- Scales.InstagramPhotoPortrait
- Scales.InstagramStories
- Scales.InstagramReels
- Scales.InstagramIGTVCoverPhoto
- Scales.InstagramVideoSquare
- Scales.InstagramVideoLandscape
- Scales.InstagramVideoPortrait

