import json

from db.session import engine
from models.gita import GitaCommentary
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

with open("../data/commentary.json", encoding="utf8") as file:
    li = []
    data = json.loads(file.read().encode("utf-8"))

    for i in data:
        li.append(
            GitaCommentary(
                description=i.get("description"),
                author_name=i.get("authorName"),
                language=i.get("lang"),
                verse_id=i.get("verseNumber"),
            )
        )
    session.add_all(li)
    session.commit()
