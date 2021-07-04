import json

from rich.progress import track
from sqlalchemy.orm import sessionmaker

from bhagavad_gita_api.data.helpers import get_file
from bhagavad_gita_api.db.session import engine
from bhagavad_gita_api.models.gita import GitaVerse

Session = sessionmaker(bind=engine)
session = Session()

content = get_file("verse.json")


li = []
data = json.loads(content)

for i in track(data, description="Loading verses"):
    li.append(
        GitaVerse(
            verse_number=i.get("verse_number"),
            chapter_number=i.get("chapter_number"),
            text=i.get("text"),
            id=i.get("id"),
            chapter_id=i.get("chapter_id"),
        )
    )
session.add_all(li)
session.commit()
