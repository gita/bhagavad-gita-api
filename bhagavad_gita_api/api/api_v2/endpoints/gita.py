import logging
import random
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session, joinedload

from bhagavad_gita_api.api import deps
from bhagavad_gita_api.models import gita as models
from bhagavad_gita_api.models import schemas

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/chapters/", response_model=List[schemas.GitaChapter], tags=["chapters"])
async def get_all_chapters(
    skip: int = 0,
    limit: int = 18,
    db: Session = Depends(deps.get_db),
):
    chapters = (
        db.query(models.GitaChapter)
        .with_entities(
            models.GitaChapter.id,
            models.GitaChapter.slug,
            models.GitaChapter.name,
            models.GitaChapter.name_transliterated,
            models.GitaChapter.name_translated,
            models.GitaChapter.verses_count,
            models.GitaChapter.chapter_number,
            models.GitaChapter.name_meaning,
            models.GitaChapter.chapter_summary,
        )
        .order_by(models.GitaChapter.id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return chapters


@router.get(
    "/chapters/{chapter_number}/", response_model=schemas.GitaChapter, tags=["chapters"]
)
async def get_particular_chapter(
    chapter_number: int, db: Session = Depends(deps.get_db)
):
    chapter = (
        db.query(models.GitaChapter)
        .filter(models.GitaChapter.chapter_number == chapter_number)
        .with_entities(
            models.GitaChapter.id,
            models.GitaChapter.slug,
            models.GitaChapter.name,
            models.GitaChapter.name_transliterated,
            models.GitaChapter.name_translated,
            models.GitaChapter.verses_count,
            models.GitaChapter.chapter_number,
            models.GitaChapter.name_meaning,
            models.GitaChapter.chapter_summary,
        )
        .first()
    )
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter


# @router.get("/verses/", response_model=List[schemas.GitaVerse], tags=["verses"])
# def get_all_verses_from_all_chapters(
#     skip: int = 0, limit: int = 10, db: Session = Depends(deps.get_db)
# ):
#     verses = (
#         db.query(models.GitaVerse)
#         .options(
#             joinedload(models.GitaVerse.commentaries),
#             joinedload(models.GitaVerse.translations),
#         )
#         .order_by(models.GitaVerse.id.asc())
#         .offset(skip)
#         .limit(limit)
#         .all()
#     )
#     return verses


@router.get(
    "/chapters/{chapter_number}/verses/",
    response_model=List[schemas.GitaVerse],
    tags=["verses"],
)
async def get_all_verses_from_particular_chapter(
    chapter_number: int, db: Session = Depends(deps.get_db)
):
    verses = (
        db.query(models.GitaVerse)
        .options(
            joinedload(models.GitaVerse.commentaries),
            joinedload(models.GitaVerse.translations),
        )
        .order_by(models.GitaVerse.id.asc())
        .filter(models.GitaVerse.chapter_number == chapter_number)
        .all()
    )
    if verses is None:
        raise HTTPException(status_code=404, detail="Verse not found")
    return verses


@router.get(
    "/chapters/{chapter_number}/verses/{verse_number}/",
    response_model=schemas.GitaVerse,
    tags=["verses"],
)
async def get_particular_verse_from_chapter(
    chapter_number: int, verse_number: int, db: Session = Depends(deps.get_db)
):
    verse = (
        db.query(models.GitaVerse)
        .options(
            joinedload(models.GitaVerse.commentaries),
            joinedload(models.GitaVerse.translations),
        )
        .filter(
            models.GitaVerse.chapter_number == chapter_number,
            models.GitaVerse.verse_number == verse_number,
        )
        .first()
    )
    if verse is None:
        raise HTTPException(status_code=404, detail="Verse not found")
    return verse


@router.get("/set-daily-verse")
async def set_daily_verse(db: Session = Depends(deps.get_db)):

    verse_number = random.randint(1, 700)

    verse = (
        db.query(models.VerseOfDay)
        .filter(
            models.VerseOfDay.date == date.today(),
        )
        .first()
    )
    if verse is None:
        li = []
        li.append(models.VerseOfDay(verse_number=verse_number, date=date.today()))
        db.add_all(li)
        db.commit()
        return Response(status_code=200, content="verse set")

    else:
        return Response(status_code=200, content="verse already set")
