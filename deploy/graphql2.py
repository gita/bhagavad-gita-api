import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
# from models import models.gitaChapterModel,models.gitaVerseModel,models.gitaVerse,models.gitaChapter
import models
from database import db_session

db = db_session.session_factory()



        


class Query(graphene.ObjectType):
    chapters = graphene.List(
        models.gitaChapterModel,
        chapterNumber=graphene.Int(),
        limit = graphene.Int(),
        first = graphene.Int(),
        skip = graphene.Int())


    verses = graphene.List(
        models.gitaVerseModel,
        verseNumber = graphene.Int(),
        limit = graphene.Int(),
        first = graphene.Int(),
        skip = graphene.Int())


    @staticmethod
    def resolve_chapters(parent, info,**kwargs):
        
        if 'chapterNumber' in kwargs.keys():
            query = models.gitaChapterModel.get_query(info).filter(models.gitaChapter.chapter_number==kwargs.get('chapterNumber'))  # SQLAlchemy query
        elif 'limit' in kwargs.keys():
            query = models.gitaChapterModel.get_query(info).limit(kwargs.get('limit'))
        else:
            
            query = models.gitaChapterModel.get_query(info)  # SQLAlchemy query
        
        if "skip" in kwargs.keys():
            query = query[kwargs.ger('skip'):]

        if 'first' in kwargs.keys():
            query = query[:kwargs.get('first')]

        return query

    @staticmethod
    def resolve_verses(parent,info,**kwargs):
        
        if 'verseNumber' in kwargs.keys():
            query = models.gitaVerseModel.get_query(info).filter(models.gitaVerse.id == kwargs.get('verseNumber'))
        elif 'limit' in kwargs.keys():
            query = models.gitaVerseModel.get_query(info).limit(kwargs.get('limit'))
        else:
            query = models.gitaVerseModel.get_query(info)
        
        if "skip" in kwargs.keys():
            query = query[kwargs.ger('skip'):]

        if 'first' in kwargs.keys():
            query = query[:kwargs.get('first')]
            
        return query


        
app = FastAPI()
app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))