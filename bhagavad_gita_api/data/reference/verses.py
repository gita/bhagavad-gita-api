from rich.progress import track

from bhagavad_gita_api.db.session import SessionLocal
from bhagavad_gita_api.models.gita import GitaChapter, GitaVerse

db = SessionLocal()


verse_objects = db.query(GitaVerse).order_by(GitaVerse.id).all()
for verse_object in track(verse_objects, description="Referencing verses"):
    chapter_number = verse_object.chapter_number
    chapter_object = (
        db.query(GitaChapter)
        .filter(GitaChapter.chapter_number == chapter_number)
        .first()
    )
    verse_object.chapter_id = chapter_object.id

db.add(verse_objects)
db.commit()
