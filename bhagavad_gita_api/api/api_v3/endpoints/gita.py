import enum
import logging
import random
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from bhagavad_gita_api.api import deps
from bhagavad_gita_api.models import gita as models
from bhagavad_gita_api.models import schemas

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)

router = APIRouter()

# https://stackoverflow.com/questions/33690064/dynamically-create-an-enum-with-custom-values-in-python
# make this dynamic and implement same logic on detailed verses, V3 would be good to go


class TranslationAuthor(enum.Enum):
    hindi_swami_ramsukhdas = "Swami Ramsukhdas"
    hindi_swami_tejomayananda = "Swami Tejomayananda"
    english_swami_adidevananda = "Swami Adidevananda"
    english_swami_gambirananda = "Swami Gambirananda"
    english_swami_sivananda = "Swami Sivananda"
    english_swami_sankranarayan = "Dr. S. Sankaranarayan"
    english_swami_purohit = "Shri Purohit Swami"


class TransliterationLanguage(enum.Enum):
    sanskrit = "sanskrit"
    telugu = "telugu"
    tamil = "tamil"
    punjabi = "punjabi"
    oriya = "oriya"
    malayalam = "malayalam"
    kannada = "kannada"
    gujarati = "gujarati"
    bengali = "bengali"


class CommentaryAuthor(enum.Enum):
    shri_abhinav_gupta = "Sri Abhinavgupta"
    shri_ananddiri = "Sri Anandgiri"
    shri_dhanpati = "Sri Dhanpati"
    shri_jayatritha = "Sri Jayatritha"
    sri_madhavacharya = "Sri Madhavacharya"
    sri_madhusudan_sarasvari = "Sri Madhusudan Saraswati"
    sri_neelkanth = "Sri Neelkanth"


@router.get(
    "/chapters/",
    response_model=List[schemas.GitaChapter],
    tags=[
        "chapters_v3",
    ],
)
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
            models.GitaChapter.chapter_summary_hindi,
        )
        .order_by(models.GitaChapter.id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return chapters


@router.get(
    "/chapters/{chapter_number}/",
    response_model=schemas.GitaChapter,
    tags=[
        "chapters_v3",
    ],
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
            models.GitaChapter.chapter_summary_hindi,
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
    response_model=List[schemas.GitaVerseV3],
    tags=["verses_v3"],
)
async def get_all_verses_from_particular_chapter(
    chapter_number: int,
    transliteration_language: TransliterationLanguage,
    translation_author: TranslationAuthor,
    commentarty_author: CommentaryAuthor,
    db: Session = Depends(deps.get_db),
):
    verses = (
        db.query(models.GitaVerse)
        .filter(models.GitaVerse.chapter_number == chapter_number)
        .order_by(models.GitaVerse.id.asc())
        .all()
    )
    res = []
    for verse in verses:
        res.append(
            schemas.GitaVerseV3(
                id=verse.id,
                verse_number=verse.verse_number,
                chapter_number=verse.chapter_number,
                slug=verse.slug,
                text=verse.text,
                transliteration=verse.transliteration,
                word_meanings=verse.word_meanings,
                sanskrit_recitation_url=verse.sanskrit_recitation_url,
                transliterations=verse.transliterations.filter(
                    models.GitaTransliteration.language
                    == transliteration_language.value
                ).all(),
                # commentaries = [verse.commentaries.filter().first()],
                translations=[
                    verse.translations.filter(
                        models.GitaTranslation.author_name == translation_author.value
                    ).first()
                ],
                commentaries=[
                    verse.commentaries.filter(
                        models.GitaCommentary.author_name == commentarty_author.value
                    ).first()
                ],
            )
        )

    if verses is None:
        raise HTTPException(status_code=404, detail="Verse not found")
    return res


@router.get(
    "/chapters/{chapter_number}/verses/{verse_number}/",
    response_model=schemas.GitaVerseV3,
    tags=["verses_v3"],
)
async def get_particular_verse_from_chapter(
    chapter_number: int,
    verse_number: int,
    transliteration_language: TransliterationLanguage,
    translation_author: TranslationAuthor,
    commentarty_author: CommentaryAuthor,
    db: Session = Depends(deps.get_db),
):
    verse = (
        db.query(models.GitaVerse)
        .filter(
            models.GitaVerse.chapter_number == chapter_number,
            models.GitaVerse.verse_number == verse_number,
        )
        .first()
    )

    if verse is None:
        raise HTTPException(status_code=404, detail="Verse not found")

    return schemas.GitaVerseV3(
        id=verse.id,
        verse_number=verse.verse_number,
        chapter_number=verse.chapter_number,
        slug=verse.slug,
        text=verse.text,
        transliteration=verse.transliteration,
        word_meanings=verse.word_meanings,
        sanskrit_recitation_url=verse.sanskrit_recitation_url,
        transliterations=verse.transliterations.filter(
            models.GitaTransliteration.language == transliteration_language.value
        ).all(),
        translations=[
            verse.translations.filter(
                models.GitaTranslation.author_name == translation_author.value
            ).first()
        ],
        commentaries=[
            verse.commentaries.filter(
                models.GitaCommentary.author_name == commentarty_author.value
            ).first()
        ],
    )


@router.get(
    "/translations/authors/all/",
    response_model=List[schemas.GitaAuthor],
    tags=["translations_v3"],
)
async def get_unique_translation_authors(db: Session = Depends(deps.get_db)):
    authors = (
        db.query(models.GitaTranslation).distinct(models.GitaTranslation.author_name)
    ).all()

    return [schemas.GitaAuthor(author_name=x.author_name) for x in authors]


@router.get(
    "/commetaries/authors/all/",
    response_model=List[schemas.GitaAuthor],
    tags=["translations_v3"],
)
async def get_unique_commentary_authors(db: Session = Depends(deps.get_db)):
    authors = (
        db.query(models.GitaCommentary).distinct(models.GitaCommentary.author_name)
    ).all()

    return [schemas.GitaAuthor(author_name=x.author_name) for x in authors]


@router.post(
    "/set-daily-verse/",
    tags=[
        "verses_v3",
    ],
)
async def set_daily_verse(db: Session = Depends(deps.get_db)):

    verse_order = random.randint(1, 700)

    verse = (
        db.query(models.VerseOfDay)
        .filter(
            models.VerseOfDay.date == date.today(),
        )
        .first()
    )

    if verse is None:
        verse_of_day = models.VerseOfDay(verse_order=verse_order, date=date.today())
        db.add(verse_of_day)
        db.commit()

        return Response(status_code=201, content="Verse of the day has been set.")

    else:
        return Response(
            status_code=200, content="Verse of the day has already been set."
        )


@router.get(
    "/get-daily-verse/",
    response_model=schemas.GitaVerseV3,
    tags=[
        "verses-v3",
    ],
)
async def get_daily_verse(db: Session = Depends(deps.get_db)):
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
                joinedload(models.GitaVerse.transliterations),
            )
            .filter(models.GitaVerse.id == verse_of_day.verse_order)
            .first()
        )

        if verse:
            print(verse)
            return verse

    raise HTTPException(status_code=404, detail="Verse of the day not found.")


@router.get(
    "/search",
    response_model=List[schemas.GitaVerseBase],
    tags=[
        "search_v3",
    ],
)
def search_gita(query: str, db: Session = Depends(deps.get_db)):
    res = (
        db.query(models.GitaVerse)
        .filter(
            or_(
                models.GitaVerse.transliteration.op("@@")(func.plainto_tsquery(query)),
                models.GitaVerse.word_meanings.op("@@")(func.plainto_tsquery(query)),
            )
        )
        .all()
    )
    res += (
        db.query(models.GitaVerse)
        .join(models.GitaTranslation)
        .filter(
            or_(
                models.GitaTranslation.author_name == "Swami Sivananda",
                models.GitaTranslation.author_name == "Dr. S. Sankaranarayan",
                models.GitaTranslation.author_name == "Shri Purohit Swami",
            )
        )
        .filter(
            models.GitaTranslation.description.op("@@")(func.plainto_tsquery(query))
        )
        .all()
    )
    return set(res)
