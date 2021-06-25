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
        limit = graphene.Int())
    verses = graphene.List(
        models.gitaVerseModel,
        verseNumber = graphene.Int(),
        limit = graphene.Int())


    @staticmethod
    def resolve_chapters(parent, info,**kwargs):
        
        if 'chapterNumber' in kwargs.keys():
            query = models.gitaChapterModel.get_query(info).filter(models.gitaChapter.ChapterNumber==kwargs.get('chapterNumber'))  # SQLAlchemy query
        if 'limit' in kwargs.keys():
            query = models.gitaChapterModel.get_query(info).limit(kwargs.get('limit'))
        else:
            query = models.gitaChapterModel.get_query(info)  # SQLAlchemy query

        return query.all()

    @staticmethod
    def resolve_verses(parent,info,**kwargs):
        
        if 'verseNumber' in kwargs.keys():
            query = models.gitaVerseModel.get_query(info).filter(models.gitaVerse.id == kwargs.get('verseNumber'))
        if 'limit' in kwargs.keys():
            query = models.gitaVerseModel.get_query(info).limit(kwargs.get('limit'))
        else:
            query = models.gitaVerseModel.get_query(info)
        return query.all()
app = FastAPI()
app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))