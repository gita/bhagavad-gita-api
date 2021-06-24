from sqlalchemy import engine
from fastapi import Depends,FastAPI,HTTPException,Request
from sqlalchemy.orm import Session
from . import  models, schemas
from .database import SessionLocal,engine
import uvicorn
from typing import List


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/gitaChapters/", response_model=List[schemas.gitaChapterBase])
def read_chapters(skip: int = 0, limit: int = 1, db: Session = Depends(get_db)):
    chapters = db.query(models.gitaChapter).offset(skip).limit(limit).all()
    return chapters

@app.get("/gitaChapters/{chapter_id}", response_model=schemas.gitaChapterBase)
def read_chapter(chapter_id: int, db: Session = Depends(get_db)):
    chapter = db.query(models.gitaChapter).filter(models.gitaChapter.id == chapter_id).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@app.get("/gitaVerses/", response_model=List[schemas.gitaVerseBase])
def read_verses(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    verses =db.query(models.gitaVerse).offset(skip).limit(limit).all()
    return verses

@app.get("/gitaVerses/{verse_id}", response_model=schemas.gitaVerseBase)
def read_verse(verse_id: int, db: Session = Depends(get_db)):
    verse = db.query(models.gitaVerse).filter(models.gitaVerse.id == verse_id).first()
    if verse is None:
        raise HTTPException(status_code=404, detail="Verse not found")
    return verse

@app.get("/gitaTranslations/", response_model=List[schemas.gitaTranslationBase])
def read_translations(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    translations = db.query(models.gitaTranslation).offset(skip).limit(limit).all()
    return translations

@app.get("/gitaTranslations/{translation_id}", response_model=schemas.gitaTranslationBase)
def read_translation(translation_id: int, db: Session = Depends(get_db)):
    translation = db.query(models.gitaTranslation).filter(models.gitaTranslation.id == translation_id).first()
    if translation is None:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation

@app.get("/gitaCommentaries/", response_model=List[schemas.gitaCommentaryBase])
def read_commentaries(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    commentaries = db.query(models.gitaCommentary).offset(skip).limit(limit).all()
    return commentaries

@app.get("/gitaCommentaries/{commentary_id}", response_model=schemas.gitaCommentaryBase)
def read_commentary(commentary_id: int, db: Session = Depends(get_db)):
    commentary = db.query(models.gitaCommentary).filter(models.gitaCommentary.id == commentary_id).first()
    if commentary is None:
        raise HTTPException(status_code=404, detail="Commentary not found")
    return commentary


@app.get("/gitaAuthors/", response_model=List[schemas.gitaAuthorBase])
def read_authors(skip: int = 0, limit: int = 2, db: Session = Depends(get_db)):
    authors = db.query(models.gitaAuthor).offset(skip).limit(limit).all()
    return authors

@app.get("/gitaAuthors/{author_id}", response_model=schemas.gitaAuthorBase)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.gitaAuthor).filter(models.gitaAuthor.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)