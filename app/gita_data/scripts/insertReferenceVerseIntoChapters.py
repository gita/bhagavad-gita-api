from db.session import SessionLocal
from models.gita import GitaChapter, GitaVerse

db = SessionLocal()

count = 0
verse_objects = db.query(GitaVerse).order_by(GitaVerse.id).all()
for verse_object in verse_objects:
    count += 1
    print(count)
    chapter_number = verse_object.chapter_number
    chapter_object = (
        db.query(GitaChapter)
        .filter(GitaChapter.chapter_number == chapter_number)
        .first()
    )
    verse_object.chapter_id = chapter_object.id

db.add(verse_objects)
db.commit()
