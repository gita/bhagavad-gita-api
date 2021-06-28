import json

from db.session import engine
from models.gita import GitaLanguage
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

with open("../data/languages.json", encoding="utf8") as file:
    li = []
    data = json.loads(file.read().encode("utf-8"))

    for i in data:
        li.append(
            GitaLanguage(
                language=i["language"],
            )
        )
    session.add_all(li)
    session.commit()
