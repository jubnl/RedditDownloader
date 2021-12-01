import json
import os
from datetime import date
from typing import List, Tuple

import praw
import requests
from environs import Env

from .ScaleImages import scale_image


class RedditBot:
    def __init__(self, env: Env, save_path=os.getcwd(), log: bool = False) -> None:
        """Reddit downloader class

        :param env: environs.Env object that already has been initialized. You can use utils.get_credentials() for that.
        :param log: True to log operations in console, by default to False.
        :param save_path: A string or pathlike to a folder where images and data will be downloaded (cwd by default).
        """

        # init YoutubeBot class
        super().__init__()

        self.log = log

        # connect to reddit
        self._reddit = praw.Reddit(
            client_id=env("REDDIT_CLIENT_ID"),
            client_secret=env("REDDIT_CLIENT_SECRET"),
            user_agent=env("REDDIT_USER_AGENT")
        )

        # define image format that we want to query
        self._accepted_format = ["jpg", "png", "gif"]

        # define a path with folder that has today's date
        self._today_data_path = os.path.join(save_path, f"data\\{date.today().strftime('%m%d%Y')}\\")

        # define path to utility file like already_downloaded.json
        self._already_downloaded_path = os.path.join(save_path, f"data/utils/")

        # define file name for already downloaded images
        self._already_downloaded_json = "already_downloaded.json"

        # create already_downloaded.json if not exists
        if not os.path.isdir(self._already_downloaded_path):
            os.makedirs(self._already_downloaded_path, exist_ok=True)
            with open(file=f"{self._already_downloaded_path}{self._already_downloaded_json}", mode="w") as f:
                pass

        # load json file to class
        with open(file=f"{self._already_downloaded_path}{self._already_downloaded_json}", mode="r") as f:
            try:
                self._already_downloaded = json.load(f)
            except json.decoder.JSONDecodeError:
                self._already_downloaded = []

    def _create_subreddit_folder(self, subreddit: str) -> str:

        sub_path = os.path.join(self._today_data_path, f"{subreddit}")
        if not os.path.isdir(sub_path):
            os.makedirs(sub_path, exist_ok=True)
            os.mkdir(os.path.join(sub_path, "images"))
            os.mkdir(os.path.join(sub_path, "data"))
        return sub_path

    def _get_posts_from_subreddit(self, subreddit: str, over_18: bool, amount: int, accepted_format: Tuple[str]) -> \
            List[praw.reddit.models.Submission]:

        submissions = []
        for submission in self._reddit.subreddit(subreddit).top("day", limit=1000):
            if not submission.stickied and submission.url.lower()[-3:] in accepted_format and \
                    submission.over_18 == over_18 and submission.id not in self._already_downloaded:
                submissions.append(submission)
            if len(submissions) >= amount:
                break
        return submissions

    @staticmethod
    def _save_submission_image(save_path: str, submission: praw.reddit.models.Submission, scale: tuple,
                               replace_resized: bool) -> None:

        img = requests.get(submission.url.lower())
        with open(save_path, "wb") as f:
            f.write(img.content)

        if scale:
            scale_image(save_path, scale, replace_resized)

    def _save_submission_data(self, save_path: str, image_path: str, submission: praw.reddit.models.Submission) -> None:
        submission.comment_sort = "best"
        best_comment = None
        best_comment_2 = None
        best_reply = None

        for comment in submission.comments:
            if len(comment.body) <= 140 and "http" not in comment.body:
                if not best_comment:
                    best_comment = comment
                else:
                    best_comment_2 = comment.body
                    break

        if best_comment:
            best_comment.reply_sort = "top"
            best_comment.refresh()

            for reply in best_comment.replies:
                if len(reply.body) >= 140 or "http" in reply.body:
                    continue
                best_reply = reply.body
                break

            best_comment = best_comment.body

        submission_data = {
            "image_path": image_path,
            'id': submission.id,
            "title": submission.title,
            "score": submission.score,
            "18": submission.over_18,
            "Best_comment": best_comment,
            "Best_comment_2": best_comment_2,
            "best_reply": best_reply
        }

        self._already_downloaded.append(submission.id)
        with open(f"{self._already_downloaded_path}{self._already_downloaded_json}", mode="w",
                  encoding="utf-8-sig") as f:
            json.dump(self._already_downloaded, f)
        with open(f"{save_path}", mode="w", encoding="utf-8-sig") as f:
            json.dump(submission_data, f)

    def save_images_from_subreddit(self, subreddits: Tuple[str] = ("memes",), amount: int = 5,
                                   filetypes: Tuple[str] = ("jpg", "png", "gif"), nsfw: bool = False,
                                   scale: tuple = None, replace_resized: bool = True) -> None:
        """Save images from multiple subreddits.

        :param subreddits: Tuple of strings that contain subreddit names (by default, will search for the /r/memes
                subreddit)
        :param amount: amount of posts to query by subreddit. 5 by default.
        :param filetypes: a tuple of accepted file types. By default : ("jpg", "png", "gif"). Warning ! Using other file
                types than those 3 may cause exceptions. That functionality haven't been tested. Its use is mainly to
                restrain queries to one or two of the default types.
        :param nsfw: True for NSFW posts only, False for SFW posts only. False by default
        :param scale: a tuple (width: int, height: int) you can pass with the new width/height (in pixel) for each image
                downloaded. None by default
        :param replace_resized: used if a scale is passed. If True it will replace the images, if False it will create a
                new directory with resized images. True by default
        :return: None
        """

        for subreddit in subreddits:
            save_path = self._create_subreddit_folder(subreddit)
            submissions = self._get_posts_from_subreddit(subreddit, nsfw, amount, filetypes)
            for submission in submissions:
                image_path = f"{save_path}\\images\\{submission.id}{submission.url.lower()[-4:]}"
                self._save_submission_image(image_path, submission, scale, replace_resized)
                self._save_submission_data(f"{save_path}\\data\\{submission.id}.json", image_path, submission)
                if self.log:
                    print(f"image downloaded from /r/{subreddit}.")
            if self.log:
                print(f"{len(submissions)} images from /r/{subreddit} have been downloaded.")
        if self.log:
            print(f"Download finished for the following subreddit(s) : {', '.join(subreddits)}.")
