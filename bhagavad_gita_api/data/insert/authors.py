import json

from rich.progress import track
from sqlalchemy.orm import sessionmaker

from bhagavad_gita_api.data.helpers import get_file
from bhagavad_gita_api.db.session import engine
from bhagavad_gita_api.models.gita import GitaAuthor

Session = sessionmaker(bind=engine)
session = Session()


content = get_file("authors.json")

li = []
data = json.loads(content)

for i in track(data, description="Loading authors"):
    li.append(
        GitaAuthor(
            name=i["name"],
            id=i["id"],
        )
    )
session.add_all(li)
session.commit()
