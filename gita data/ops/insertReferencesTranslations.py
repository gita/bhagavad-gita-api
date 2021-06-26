
from api.database import engine
from sqlalchemy import  select
from sqlalchemy.orm import  sessionmaker
from api.models import gitaTranslation, gitaVerse, gitaAuthor, gitaLanguage

Session = sessionmaker(bind=engine)
session = Session()     
Counter = 0
translations = session.execute(select(gitaTranslation).order_by(gitaTranslation.id))
for translation_object in translations.scalars():
    Counter+=1
    print(Counter)
    try:
        versenumber = translation_object.verseNumber
        verse = session.execute(select(gitaVerse).filter_by(verse_order=versenumber)).scalar_one()

        languageInComm = translation_object.lang
        languageObject = session.execute(select(gitaLanguage).filter_by(language=languageInComm)).scalar_one()

        author_name = translation_object.authorName
        authorObject = session.execute(select(gitaAuthor).filter_by(name=author_name)).scalar_one()

        translation_object.author_id = authorObject.id
        translation_object.language_id = languageObject.id
        translation_object.verse_id = verse.id
    except :
        print("err Author not found ",author_name , "Translation "+ str(translation_object.id))
    # print(f"{authorObject.name} {languageObject.language} {verse.text}")

session.commit()


