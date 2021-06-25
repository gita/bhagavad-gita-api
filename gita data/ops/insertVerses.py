import json
from api.database import engine
from sqlalchemy import  MetaData
from sqlalchemy.orm import  sessionmaker
from api.models import gitaChapter, gitaVerse

Session = sessionmaker(bind=engine)
session = Session()     

# meta = MetaData()

with open('data/verse.json','r',encoding='utf8') as file:
        
    
    li = []
    data = json.loads(file.read().encode('utf-8'))

    for i in data:
        li.append(gitaVerse(
            externalId=i.get('externalId'),
            title=i.get('title'),
            verse_order = i.get('verse_order'),
            verse_number = i.get('verse_number'),
            chapter_number = i.get('chapter_number'),
            text = i.get('text'),
        
        )) 
    session.add_all(li)
    session.commit()
   