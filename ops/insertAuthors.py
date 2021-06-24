import json
from api.database import engine
from sqlalchemy import  MetaData
from sqlalchemy.orm import  sessionmaker
from api.models import gitaChapter,gitaAuthor

Session = sessionmaker(bind=engine)
session = Session()     

# meta = MetaData()

with open('data/authors.json','r',encoding='utf8') as file:
        
    
    li = []
    data = json.loads(file.read().encode('utf-8'))

    for i in data:
        li.append(gitaAuthor(
            
            name = i['name'],          
        )) 
    session.add_all(li)
    session.commit()
   