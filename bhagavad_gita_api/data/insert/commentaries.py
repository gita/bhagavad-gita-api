import json

from rich.progress import track
from sqlalchemy.orm import sessionmaker

from bhagavad_gita_api.data.helpers import get_file
from bhagavad_gita_api.db.session import engine
from bhagavad_gita_api.models.gita import GitaCommentary

Session = sessionmaker(bind=engine)
session = Session()

content = get_file("commentary.json")


li = []
data = json.loads(content)

for i in track(data, description="Loading commentary"):
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
