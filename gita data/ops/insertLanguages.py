import json
from api.database import engine
from sqlalchemy import  MetaData
from sqlalchemy.orm import  sessionmaker
from api.models import gitaLanguage

Session = sessionmaker(bind=engine)
session = Session()     

# meta = MetaData()

with open('data/languages.json','r',encoding='utf8') as file:
        
    
    li = []
    data = json.loads(file.read().encode('utf-8'))

    for i in data:
        li.append(gitaLanguage(
            
            language = i['language'],          
        )) 
    session.add_all(li)
    session.commit()
   