from environs import Env


class Scales:
    """Some known format are already defined here. You can use them by importing Scales from utils.

    """
    # youtube format
    YoutubeShortsFullscreen = (1080, 1920)
    YoutubeShortsSquare = (1080, 1080)
    YoutubeVideo = (1920, 1080)

    # tiktok format
    TikTok = YoutubeShortsFullscreen

    # instagram format
    InstagramPhotoSquare = YoutubeShortsSquare
    InstagramPhotoLandscape = (1080, 608)
    InstagramPhotoPortrait = (1080, 1350)
    InstagramStories = YoutubeShortsFullscreen
    InstagramReels = InstagramStories
    InstagramIGTVCoverPhoto = (420, 654)
    InstagramVideoSquare = InstagramPhotoSquare
    InstagramVideoLandscape = (1080, 608)
    InstagramVideoPortrait = InstagramPhotoPortrait


def get_credentials():
    env = Env()
    env.read_env()
    return env
