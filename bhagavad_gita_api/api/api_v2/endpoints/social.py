import logging
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session, joinedload

from bhagavad_gita_api.api import deps
from bhagavad_gita_api.models import gita as models

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.post("/post-on-instagram/", tags=["social"])
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
            .options(
                joinedload(models.GitaVerse.commentaries),
                joinedload(models.GitaVerse.translations),
            )
            .filter(models.GitaVerse.id == verse_of_day.verse_order)
            .first()
        )

        if verse:
            # CALL INSTAGRAM POSTING FUNCTION HERE
            return Response(
                status_code=201,
                content="Verse of the day has been posted on Instagram.",
            )

    raise HTTPException(status_code=404, detail="Verse of the day not found.")
