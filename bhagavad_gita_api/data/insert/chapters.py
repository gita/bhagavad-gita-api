import json

from rich.progress import track
from sqlalchemy.orm import sessionmaker

from bhagavad_gita_api.data.helpers import get_file
from bhagavad_gita_api.db.session import engine
from bhagavad_gita_api.models.gita import GitaChapter

Session = sessionmaker(bind=engine)
session = Session()

content = get_file("chapters.json")

li = []
data = json.loads(content)

for i in track(data, description="Loading chapters"):
    li.append(
        GitaChapter(
            id=i["id"],
            name=i["name"],
            name_transliterated=i["name_transliterated"],
            name_translated=i["name_translation"],
            verses_count=i["verses_count"],
            chapter_number=i["chapter_number"],
            name_meaning=i["name_meaning"],
            chapter_summary=i["chapter_summary"],
            slug=f'chapter-{i["chapter_number"]}-{i["name_translation"].replace(" ", "-").lower()}',
        )
    )
session.add_all(li)
session.commit()
