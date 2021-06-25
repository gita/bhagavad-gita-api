from sqlalchemy.sql.functions import count
from api.database import engine
from sqlalchemy import  select
from sqlalchemy.orm import  sessionmaker
from api.models import gitaChapter, gitaVerse

Session = sessionmaker(bind=engine)
session = Session()     
cou  = 0
verses = session.execute(select(gitaVerse).order_by(gitaVerse.id))
for verse_object in verses.scalars():
    cou +=1
    print(cou)
    chapternumber = verse_object.chapter_number
    chapter = session.execute(select(gitaChapter).filter_by(chapter_number=chapternumber)).scalar_one()
    # print(f"{chapter.chapter_number}")
    verse_object.chapter_id = chapter.id

session.commit()


