import time
import praw
import os
import json
import random
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, timedelta
from my_prompts import *


class CommentBot:
    def __init__(self):
        load_dotenv()
        self.reddit = praw.Reddit(
            client_id=os.getenv("reddit_client_id"),
            client_secret=os.getenv("reddit_client_secret"),
            username=os.getenv("reddit_username"),
            password=os.getenv("reddit_password"),
            user_agent="reddit_bot",
            ratelimit_seconds=300,
        )
        self.subreddit_name = "askreddit"
        self.commented_posts = self.load_commented_posts()

    def load_commented_posts(self):
        try:
            with open("data/commented_posts.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_commented_posts(self):
        with open("data/commented_posts.json", "w") as file:
            json.dump(self.commented_posts, file, indent=4)

    def get_recent_posts(self, limit=30):
        subreddit = self.reddit.subreddit(self.subreddit_name)
        new_posts = list(subreddit.new(limit=limit))
        return list(
            filter(lambda post: post.score > 5 or post.num_comments > 5, new_posts)
        )

    def is_valid_post(self, post):
        current_time = datetime.now()
        post_created_datetime = datetime.fromtimestamp(post.created)
        time_difference = current_time - post_created_datetime

        if time_difference > timedelta(hours=3) and time_difference > timedelta(
            minutes=15
        ):
            return False
        if post.id in self.commented_posts:
            return False

        is_moderator = post.author_flair_text and (
            "mod" in post.author_flair_text.lower()
            and "bot" not in post.author_flair_text.lower()
        )
        is_invalid_post = post.is_video or is_moderator

        return not is_invalid_post

    def generate_comment(self, post):
        prompt = get_comment_to_post_prompt(post)
        client = OpenAI(api_key=os.getenv("openai_api_key"))

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful Reddit user who comments helpful and valuable answers on Reddit posts.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=2000,
            temperature=0,
            model="gpt-4",
        )

        response = completion.choices[0].message.content.strip()
        if len(response.split("\n")) > 1:
            response = "\n".join(response.split("\n")[:-1])
        return response

    def reply_to_post(self, post, response):
        post.reply(response)

    def process_post(self, post):
        response = self.generate_comment(post)
        self.reply_to_post(post, response)
        self.commented_posts.append(post.id)

    def process_posts(self):
        posts = self.get_recent_posts(30)
        while True and len(posts) > 0:
            selected_post = random.choice(posts)
            if self.is_valid_post(selected_post):
                self.process_post(selected_post)
                self.save_commented_posts()
                posts.remove(selected_post)
                time.sleep(random.randint(700, 900))
                break
            else:
                posts.remove(selected_post)
            

    def run(self):
        while True:
            self.process_posts()


if __name__ == "__main__":
    bot = CommentBot()
    bot.run()
