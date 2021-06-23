import json
from database import engine
from sqlalchemy import  MetaData
from sqlalchemy.orm import  sessionmaker
from models import gitaChapter

Session = sessionmaker(bind=engine)
session = Session()     

# meta = MetaData()

with open('data/chapters.json','r',encoding='utf8') as file:
        
    
    li = []
    data = json.loads(file.read().encode('utf-8'))

    for i in data:
        li.append(gitaChapter(
            id=i['id'],
            name=i['name'],
            name_transliterated = i['name_transliterated'],
            name_translation = i['name_translation'],
            verses_count = i['verses_count'],
            chapter_number = i['chapter_number'],
            name_meaning = i['name_meaning'],
            image_name = i['image_name'],
            chapter_summary = i['chapter_summary'],          
        )) 
    session.add_all(li)
    session.commit()
   