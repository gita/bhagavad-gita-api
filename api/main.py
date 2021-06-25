from sqlalchemy import engine
from fastapi import Depends,FastAPI,HTTPException,Request
from sqlalchemy.orm import Session,joinedload
from . import  models, schemas
from .database import SessionLocal,engine
import uvicorn
from typing import List
import graphene
from starlette.graphql import GraphQLApp
from .graphql import Query


models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Bhagavad Gita API",
    description="The Bhagavad Gita Application Programming Interface (API) allows a web or mobile developer to use the Bhagavad Gita text in their web or mobile application(s). It is a RESTful API that follows some of the Best Practices for designing a REST API which makes it easy for developers to use and implement.",
    version="2.0",
)
app.add_route('/graphql', GraphQLApp(schema=graphene.Schema(query=Query)))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/gitaChapters/", response_model=List[schemas.gitaChapter], tags=["chapters"])
def get_all_chapters(skip: int = 0, limit: int = 18, db: Session = Depends(get_db)):
    chapters = db.query(models.gitaChapter).offset(skip).limit(limit).all()
    return chapters

@app.get("/gitaChapters/{chapter_number}", response_model=schemas.gitaChapter, tags=["chapters"])
def get_particular_chapter(chapter_number: int, db: Session = Depends(get_db)):
    chapter = db.query(models.gitaChapter).filter(models.gitaChapter.id == chapter_number).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@app.get("/gitaVerses/", response_model=List[schemas.gitaVerse], tags=["verses"])
def get_all_verses_from_all_chapters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    verses =db.query(models.gitaVerse).options(joinedload(models.gitaVerse.commentaries),joinedload(models.gitaVerse.translations)).offset(skip).limit(limit).all()
    return verses

@app.get("/gitaVerses/{verse_id}", response_model=schemas.gitaVerse, tags=["verses"])
def get_particular_verse(verse_id: int, db: Session = Depends(get_db)):
    verse = db.query(models.gitaVerse).options(joinedload(models.gitaVerse.commentaries),joinedload(models.gitaVerse.translations)).filter(models.gitaVerse.id == verse_id).first()
    if verse is None:
        raise HTTPException(status_code=404, detail="Verse not found")
    return verse

@app.get("/gitaChapters/{chapter_number}/gitaVerses/", response_model=List[schemas.gitaVerse], tags=["verses"])
def get_all_verses_from_particular_chapter(chapter_number: int, db: Session = Depends(get_db)):
    verses = db.query(models.gitaVerse).options(joinedload(models.gitaVerse.commentaries),joinedload(models.gitaVerse.translations)).filter(models.gitaVerse.chapter_number == chapter_number).all()
    if verses is None:
        raise HTTPException(status_code=404, detail="Verse not found")
    return verses

@app.get("/gitaChapters/{chapter_number}/gitaVerses/{verse_number}", response_model=schemas.gitaVerse, tags=["verses"])
def get_particular_verse_from_chapter(chapter_number: int,verse_number: int, db: Session = Depends(get_db)):
    verse = db.query(models.gitaVerse).options(joinedload(models.gitaVerse.commentaries),joinedload(models.gitaVerse.translations)).filter(models.gitaVerse.chapter_number == chapter_number , models.gitaVerse.verse_number == verse_number ).first()
    if verse is None:
        raise HTTPException(status_code=404, detail="Verse not found")
    return verse


# @app.get("/gitaTranslations/", response_model=List[schemas.gitaTranslationBase])
# def get_translations(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
#     translations = db.query(models.gitaTranslation).offset(skip).limit(limit).all()
#     return translations

# @app.get("/gitaTranslations/{translation_id}", response_model=schemas.gitaTranslationBase)
# def get_translation(translation_id: int, db: Session = Depends(get_db)):
#     translation = db.query(models.gitaTranslation).filter(models.gitaTranslation.id == translation_id).first()
#     if translation is None:
#         raise HTTPException(status_code=404, detail="Translation not found")
#     return translation

# @app.get("/gitaCommentaries/", response_model=List[schemas.gitaCommentaryBase])
# def get_commentaries(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
#     commentaries = db.query(models.gitaCommentary).offset(skip).limit(limit).all()
#     return commentaries

# @app.get("/gitaCommentaries/{commentary_id}", response_model=schemas.gitaCommentaryBase)
# def get_commentary(commentary_id: int, db: Session = Depends(get_db)):
#     commentary = db.query(models.gitaCommentary).filter(models.gitaCommentary.id == commentary_id).first()
#     if commentary is None:
#         raise HTTPException(status_code=404, detail="Commentary not found")
#     return commentary


# @app.get("/gitaAuthors/", response_model=List[schemas.gitaAuthorBase])
# def get_authors(skip: int = 0, limit: int = 2, db: Session = Depends(get_db)):
#     authors = db.query(models.gitaAuthor).offset(skip).limit(limit).all()
#     return authors

# @app.get("/gitaAuthors/{author_id}", response_model=schemas.gitaAuthorBase)
# def get_author(author_id: int, db: Session = Depends(get_db)):
#     author = db.query(models.gitaAuthor).filter(models.gitaAuthor.id == author_id).first()
#     if author is None:
#         raise HTTPException(status_code=404, detail="Author not found")
#     return author


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)