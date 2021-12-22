import json
import os

from rich.progress import track
from sqlalchemy.orm import sessionmaker

from bhagavad_gita_api.data.helpers import get_file
from bhagavad_gita_api.db.session import engine
from bhagavad_gita_api.models.gita import GitaVerse

Session = sessionmaker(bind=engine)
session = Session()

content = get_file("verse.json")
SANSKRIT_RECITATION_HOST = os.getenv("SANSKRIT_RECITATION_HOST")

li = []
data = json.loads(content)

for i in track(data, description="Loading verses"):
    li.append(
        GitaVerse(
            verse_number=i["verse_number"],
            chapter_number=i["chapter_number"],
            text=i["text"],
            sanskrit_recitation_url=f'{SANSKRIT_RECITATION_HOST}/{i["chapter_number"]}/{i["verse_number"]}.mp3',
            id=i["id"],
            chapter_id=i["chapter_id"],
            transliteration=i["transliteration"],
            word_meanings=i["word_meanings"],
            slug=f'chapter-{i["chapter_number"]}-verse-{i["verse_number"]}',
        )
    )
session.add_all(li)
session.commit()
