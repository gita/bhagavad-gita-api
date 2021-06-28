from db.session import SessionLocal
from models.gita import GitaAuthor, GitaLanguage, GitaTranslation, GitaVerse

db = SessionLocal()

count = 0
translation_objects = db.query(GitaTranslation).order_by(GitaTranslation.id).all()
for translation_object in translation_objects:
    count += 1
    print(count)

    verse_number = translation_object.verse_number
    verse_object = db.query(GitaVerse).filter(GitaVerse.id == verse_number).first()

    language_in_translation = translation_object.language
    language_object = (
        db.query(GitaLanguage)
        .filter(GitaLanguage.language == language_in_translation)
        .first()
    )

    author_name = translation_object.author_name
    author_object = db.query(GitaAuthor).filter(GitaAuthor.name == author_name).first()

    translation_object.author_id = author_object.id
    translation_object.language_id = language_object.id
    # translation_object.verse_id = verse_object.id

db.bulk_save_objects(translation_objects)
db.commit()
