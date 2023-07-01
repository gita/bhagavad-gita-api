import json

from rich.progress import track
from sqlalchemy.orm import sessionmaker

from bhagavad_gita_api.data.helpers import get_file
from bhagavad_gita_api.db.session import engine
from bhagavad_gita_api.models.gita import GitaLanguage

Session = sessionmaker(bind=engine)
session = Session()

content = get_file("languages.json")

li = []
data = json.loads(content)

languages = session.query(GitaLanguage).with_entities(GitaLanguage.id).all()
languages = [i[0] for i in languages]
for i in track(data, description="Loading languages"):

    if not i["id"] in languages:
        li.append(
            GitaLanguage(
                language=i["language"],
                id=i["id"],
            )
        )
session.add_all(li)
session.commit()
