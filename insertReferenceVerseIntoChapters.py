
from database import engine
from sqlalchemy import  select
from sqlalchemy.orm import  sessionmaker
from models import gitaChapter, gitaVerse

Session = sessionmaker(bind=engine)
session = Session()     

verses = session.execute(select(gitaVerse).order_by(gitaVerse.id))
for verse_object in verses.scalars():
    chapternumber = verse_object.chapter_number
    chapter = session.execute(select(gitaChapter).filter_by(chapter_number=chapternumber)).scalar_one()
    # print(f"{chapter.chapter_number}")
    verse_object.chapter_id = chapter.id

session.commit()


