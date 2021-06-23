
from database import engine
from sqlalchemy import  select
from sqlalchemy.orm import  sessionmaker
from models import gitaCommentary, gitaVerse, gitaAuthor, gitaLanguage

Session = sessionmaker(bind=engine)
session = Session()     

commentaries = session.execute(select(gitaCommentary).order_by(gitaCommentary.id))
for commentary_object in commentaries.scalars():
    # chapternumber = commentary_object.chapter_number
    versenumber = commentary_object.verseNumber
    verse = session.execute(select(gitaVerse).filter_by(verse_order=versenumber)).scalar_one()

    languageInComm = commentary_object.lang
    languageObject = session.execute(select(gitaLanguage).filter_by(language=languageInComm)).scalar_one()

    author_name = commentary_object.authorName
    authorObject = session.execute(select(gitaAuthor).filter_by(name=author_name)).scalar_one()

    commentary_object.author_id = authorObject.id
    commentary_object.language_id = languageObject.id
    commentary_object.verse_id = verse.id
    # print(f"{authorObject.name} {languageObject.language} {verse.text}")

session.commit()


