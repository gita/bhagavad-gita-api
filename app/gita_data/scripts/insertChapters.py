import json

from db.session import engine
from models.gita import GitaChapter
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

with open("../data/chapters.json", encoding="utf8") as file:
    li = []
    data = json.loads(file.read().encode("utf-8"))

    for i in data:
        li.append(
            GitaChapter(
                id=i["id"],
                name=i["name"],
                name_transliterated=i["name_transliterated"],
                name_translated=i["name_translated"],
                verses_count=i["verses_count"],
                chapter_number=i["chapter_number"],
                name_meaning=i["name_meaning"],
                chapter_summary=i["chapter_summary"],
            )
        )
    session.add_all(li)
    session.commit()
