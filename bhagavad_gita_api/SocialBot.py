from io import BytesIO
import random
import requests
import os

import tweepy
from PIL import Image, ImageDraw, ImageFont
from textwrap3 import wrap
from discord import Webhook, RequestsWebhookAdapter, File

from bhagavad_gita_api.config import settings
from bhagavad_gita_api.models import gita as models
from bhagavad_gita_api.MyIGBot import MyIGBot


class SocialBot:
    sanskrit_text: str
    translation_hindi: str
    translation_english: str
    output_path = BytesIO()

    def __init__(self, verse, translations):
        self.translation_english = (
            translations.filter(models.GitaTranslation.author_name == "Swami Sivananda")
            .first()
            .description
        ).replace("\n", " ")

        self.translation_hindi = (
            translations.filter(
                models.GitaTranslation.author_name == "Swami Ramsukhdas"
            )
            .first()
            .description
        ).replace("\n", " ")

        self.sanskrit_text = verse.text.replace("\n", " ")
        self.create_image_post(text=self.translation_english)

    def create_image_post(self, text):

        """
        usign pillow to add text on an image template, adjusting font
        size and line width to avoid overflows
        """
        template_num = random.randint(1, int(requests.get(settings.SOCIAL_BOT_MEDIA_URL+'template_num.txt').content))
        template = requests.get(settings.SOCIAL_BOT_MEDIA_URL+"templates/"+str(template_num)+".jpg",allow_redirects=True).content
        font_path = BytesIO(requests.get(settings.SOCIAL_BOT_MEDIA_URL+"helveticaneue.ttf", allow_redirects=True).content)
        img = Image.open(BytesIO(template))
        draw = ImageDraw.Draw(img)
        font_size = 40
        font = ImageFont.truetype(
            font_path, font_size
        )

        lines = wrap(text=text, width=50)

        line_width, line_height = font.getsize(lines[0])

        text_height = len(lines) * line_height

        while text_height > 250:
            print("in the loop")
            font_size -= 5
            font = ImageFont.truetype(
                font_path, font_size
            )
            line_height -= 10
            text_height = len(lines) * line_height

        y_text = 805

        image_width, image_height = img.size

        for line in lines:
            line_width, line_height = font.getsize(line)
            draw.text(
                ((image_width - line_width) / 2, y_text),
                line,
                font=font,
                fill=(0, 0, 0),
            )
            y_text += line_height
        rgb_im = img.convert("RGB")
        rgb_im.save(self.output_path, format="PNG")
        rgb_im.save("bhagavad_gita_api/media/output/output.png")
        self.output_path.seek(0)
        print("image created")

    def post_on_discord(self):
        """Posts on discord server in Gita-Social-Bot channel"""
        post_text = f"""
            Glories To Shri Hari \n
            Sanskrit text : {self.sanskrit_text} \n
            Hindi translation: {self.translation_hindi}\n
            """
        controller = Webhook.from_url(settings.DISCORD_WEBHOOK, adapter=RequestsWebhookAdapter())
        try:
            controller.send(post_text,file=File(self.output_path, "output.png"))
            print("Posted")
            return 200
        except Exception as e:
            return e

    def post_on_twitter(self):
        auth = tweepy.OAuthHandler(
            settings.TWITTER["CONSUMER_KEY"], settings.TWITTER["CONSUMER_SECRET"]
        )
        auth.set_access_token(
            settings.TWITTER["ACCESS_TOKEN"], settings.TWITTER["ACCESS_TOKEN_SECRET"]
        )
        api = tweepy.API(auth)
        media = api.media_upload(file=self.output_path, filename='output.png')
        try:
            tweet_text = "Glories To Shri Hari"
            post_result = api.update_status(
                status=tweet_text, media_ids=[media.media_id_string]
            )

            tweet_text = "Sanskrit Text : " + self.sanskrit_text
            sanskrit_text = api.update_status(
                status=tweet_text,
                in_reply_to_status_id=post_result.id,
                auto_populate_reply_metadata=True,
            )

            tweet_text = "Hindi Translation : " + self.translation_hindi
            hindi_text = api.update_status(
                status=tweet_text,
                in_reply_to_status_id=sanskrit_text.id,
                auto_populate_reply_metadata=True,
            )
            print(hindi_text)
            return 200

        except Exception as e:
            return e

    def post_on_instagram(self):

        # remove cookie if exists, package throws error on expired cookie
        if os.path.exists("cookie_iiradhakrishnaii.bot"):
            os.remove("cookie_iiradhakrishnaii.bot")
        else:
            pass

        try:
            caption = f"""
            Glories To Shri Hari \n
            Sanskrit text : {self.sanskrit_text} \n
            Hindi translation: {self.translation_hindi}\n
            """
            bot = MyIGBot(
                settings.INSTAGRAM["USERNAME"], settings.INSTAGRAM["PASSWORD"]
            )
            response = bot.upload_post(
                "bhagavad_gita_api/media/output/output.png", caption=caption
            )
            print(response)  # if the response code is 200 that means ok

            return 200
        except Exception:
            return 500
