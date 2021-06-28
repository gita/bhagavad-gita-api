from api import deps
from api.api_v2.api import api_router
from config import settings
from crud import get_valid_api_keys
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session

# from graphql2 import Query


API_KEY_NAME = "X-API-KEY"
api_key_header_auth = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(
    db: Session = Depends(deps.get_db),
    api_key_header: str = Security(api_key_header_auth),
) -> None:
    if api_key_header not in get_valid_api_keys(db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key.",
        )


app = FastAPI(
    title="Bhagavad Gita API",
    description="The Bhagavad Gita Application Programming Interface (API) "
    "allows a web or mobile developer to use the Bhagavad Gita text "
    "in their web or mobile application(s). It is a RESTful API that "
    "follows some of the Best Practices for designing a REST API which "
    "makes it easy for developers to use and implement.",
    version="2.0",
    dependencies=[Security(get_api_key, scopes=["openid"])],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.get("/chapters/", response_model=List[schemas.GitaChapter], tags=["chapters"])
# def get_all_chapters(skip: int = 0, limit: int = 18, db: Session = Depends(get_db)):
#     chapters = (
#         db.query(models.GitaChapter)
#         .order_by(models.GitaChapter.id.asc())
#         .offset(skip)
#         .limit(limit)
#         .all()
#     )
#     return chapters


# @app.get(
#     "/chapters/{chapter_number}/",
#     response_model=schemas.GitaChapter,
#     tags=["chapters"],
# )
# def get_particular_chapter(chapter_number: int, db: Session = Depends(get_db)):
#     chapter = (
#         db.query(models.GitaChapter)
#         .filter(models.GitaChapter.chapter_number == chapter_number)
#         .first()
#     )
#     if chapter is None:
#         raise HTTPException(status_code=404, detail="Chapter not found")
#     return chapter


# @app.get("/verses/", response_model=List[schemas.GitaVerse], tags=["verses"])
# def get_all_verses_from_all_chapters(
#     skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
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


# @app.get(
#     "/chapters/{chapter_number}/verses/",
#     response_model=List[schemas.GitaVerse],
#     tags=["verses"],
# )
# def get_all_verses_from_particular_chapter(
#     chapter_number: int, db: Session = Depends(get_db)
# ):
#     verses = (
#         db.query(models.GitaVerse)
#         .options(
#             joinedload(models.GitaVerse.commentaries),
#             joinedload(models.GitaVerse.translations),
#         )
#         .order_by(models.GitaVerse.id.asc())
#         .filter(models.GitaVerse.chapter_number == chapter_number)
#         .all()
#     )
#     if verses is None:
#         raise HTTPException(status_code=404, detail="Verse not found")
#     return verses


# @app.get(
#     "/chapters/{chapter_number}/verses/{verse_number}/",
#     response_model=schemas.GitaVerse,
#     tags=["verses"],
# )
# def get_particular_verse_from_chapter(
#     chapter_number: int, verse_number: int, db: Session = Depends(get_db)
# ):
#     verse = (
#         db.query(models.GitaVerse)
#         .options(
#             joinedload(models.GitaVerse.commentaries),
#             joinedload(models.GitaVerse.translations),
#         )
#         .filter(
#             models.GitaVerse.chapter_number == chapter_number,
#             models.GitaVerse.verse_number == verse_number,
#         )
#         .first()
#     )
#     if verse is None:
#         raise HTTPException(status_code=404, detail="Verse not found")
#     return verse

app.include_router(api_router, prefix=settings.API_V2_STR)
