import json

from db.session import engine
from models.gita import GitaVerse
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

with open("../data/verse.json", encoding="utf8") as file:
    li = []
    data = json.loads(file.read().encode("utf-8"))

    for i in data:
        li.append(
            GitaVerse(
                verse_number=i.get("verse_number"),
                chapter_number=i.get("chapter_number"),
                text=i.get("text"),
            )
        )
    session.add_all(li)
    session.commit()
