import json

from rich.progress import track
from sqlalchemy.orm import sessionmaker

from bhagavad_gita_api.data.helpers import get_file
from bhagavad_gita_api.db.session import engine
from bhagavad_gita_api.models.gita import GitaTransliteration

Session = sessionmaker(bind=engine)
session = Session()

content = get_file("transliteration.json")


li = []
data = json.loads(content)

for i in track(data, description="Loading transliterations"):
    li.append(
        GitaTransliteration(
            description=i["description"],
            language=i["lang"],
            verse_id=i["verseNumber"],
            language_id=i["language_id"],
        )
    )
session.add_all(li)
session.commit()
