import logging
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from bhagavad_gita_api.api import deps
from bhagavad_gita_api.models import gita as models

# from bhagavad_gita_api.utils import post_on_instagram,post_on_twitter
from bhagavad_gita_api.SocialBot import SocialBot

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.post("/post_verse_of_the_day/", tags=["social"])
async def post_instagram(db: Session = Depends(deps.get_db)):
    verse_of_day = (
        db.query(models.VerseOfDay)
        .filter(
            models.VerseOfDay.date == date.today(),
        )
        .first()
    )

    if verse_of_day:
        verse = (
            db.query(models.GitaVerse)
            .join(models.GitaTranslation)
            .filter(models.GitaVerse.id == verse_of_day.verse_order)
            .first()
        )

        if verse:

            # CALL INSTAGRAM POSTING FUNCTION HERE
            translations = db.query(models.GitaTranslation).filter(
                models.GitaTranslation.verse_id == verse.id
            )
            bot = SocialBot(verse, translations)
            twitter_response = bot.post_on_twitter()
            instagram_response = bot.post_on_instagram()
            discord_response = bot.post_on_discord()

            if twitter_response == 200 and instagram_response == 200 and discord_response == 200:
                return Response(
                    status_code=201,
                    content="Verse of the day has been posted on Instagram, twitter and Discord.",
                )
            else:
                HTTPException(
                    status_code=500, detail="internal server error in posting "
                )

    raise HTTPException(status_code=404, detail="Verse of the day not found.")
