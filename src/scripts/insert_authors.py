import json

from db.session import engine
from models.gita import GitaAuthor
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

with open("gita_data/authors.json", encoding="utf8") as file:
    li = []
    data = json.loads(file.read().encode("utf-8"))

    for i in data:
        li.append(
            GitaAuthor(
                name=i["name"],
            )
        )
    session.add_all(li)
    session.commit()
