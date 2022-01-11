import datetime

import pytz
from myigbot import MyIGBot
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator
from textwrap3 import wrap

from bhagavad_gita_api.models import gita as models


def tzware_datetime():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    return datetime.datetime.now(pytz.utc)


class AwareDateTime(TypeDecorator):
    """
    A DateTime type which can only store tz-aware DateTimes.

    Source:
      https://gist.github.com/inklesspen/90b554c864b99340747e
    """

    cache_ok = True
    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime.datetime) and value.tzinfo is None:
            raise ValueError("{!r} must be TZ-aware".format(value))
        return value

    def __repr__(self):
        return "AwareDateTime()"


def post_on_instagram(verse, translations):

    # print(verse)
    text = (
        translations.filter(models.GitaTranslation.author_name == "Swami Sivananda")
        .first()
        .description
    )

    hindi_text = (
        translations.filter(models.GitaTranslation.author_name == "Swami Ramsukhdas")
        .first()
        .description
    )
    sanskrit_text = verse.text
    caption = f"""
        \n Hare Krishna \n
         Original Verse: \n
            {sanskrit_text}
        \n
        Hindi Translation:\n
            {hindi_text}
        \n \n
    """

    create_image_post(text)

    print("Image created")
    bot = MyIGBot("iiradhakrishnaii", "BankeBihari100")
    response = bot.upload_post(
        "bhagavad_gita_api/media/images/output.jpg", caption=caption
    )
    print(response)  # if the response code is 200 that means ok

    return 200


def create_image_post(text):
    """
    usign pillow to add text on an image template, adjusting font
    size and line width to avoid overflows
    """
    img = Image.open("bhagavad_gita_api/media/images/template.jpg")
    draw = ImageDraw.Draw(img)
    font_size = 40
    font = ImageFont.truetype("bhagavad_gita_api/media/helveticaneue.ttf", font_size)

    lines = wrap(text=text, width=50)

    line_width, line_height = font.getsize(lines[0])

    text_height = len(lines) * line_height

    while text_height > 250:
        print("in the loop")
        font_size -= 5
        font = ImageFont.truetype(
            "bhagavad_gita_api/media/helveticaneue.ttf", font_size
        )
        line_height -= 10
        text_height = len(lines) * line_height

    print(font_size)
    y_text = 805

    image_width, image_height = img.size

    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(
            ((image_width - line_width) / 2, y_text), line, font=font, fill=(0, 0, 0)
        )
        y_text += line_height
    rgb_im = img.convert("RGB")
    rgb_im.save("bhagavad_gita_api/media/images/output.jpg")


def create_video_post():
    pass
