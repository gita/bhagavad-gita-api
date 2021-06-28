from db.session import SessionLocal
from models.gita import GitaAuthor, GitaCommentary, GitaLanguage, GitaVerse

db = SessionLocal()

count = 0
commentary_objects = db.query(GitaCommentary).order_by(GitaCommentary.id).all()
for commentary_object in commentary_objects:
    count += 1
    print(count)

    verse_number = commentary_object.verse_number
    verse_object = db.query(GitaVerse).filter(GitaVerse.id == verse_number).first()

    language_in_commentary = commentary_object.language
    language_object = (
        db.query(GitaLanguage)
        .filter(GitaLanguage.language == language_in_commentary)
        .first()
    )

    author_name = commentary_object.author_name
    author_object = db.query(GitaAuthor).filter(GitaAuthor.name == author_name).first()

    commentary_object.author_id = author_object.id
    commentary_object.language_id = language_object.id
    # commentary_object.verse_id = verse_object.id

db.bulk_save_objects(commentary_objects)
db.commit()
