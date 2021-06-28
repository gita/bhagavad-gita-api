import time

import graphene
import models
from app.db.session import db_session
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

db = db_session.session_factory()


class Query(graphene.ObjectType):
    chapters = graphene.List(
        models.GitaChapterModel,
        chapterNumber=graphene.Int(),
        limit=graphene.Int(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    verses = graphene.List(
        models.GitaVerseModel,
        verseNumber=graphene.Int(),
        limit=graphene.Int(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    @staticmethod
    def resolve_chapters(parent, info, **kwargs):
        start_time = time.time()

        if "chapterNumber" in kwargs.keys():
            query = models.GitaChapterModel.get_query(info).filter(
                models.GitaChapter.chapter_number == kwargs.get("chapterNumber")
            )  # SQLAlchemy query
        elif "limit" in kwargs.keys():
            query = models.GitaChapterModel.get_query(info).limit(kwargs.get("limit"))
        else:

            query = models.GitaChapterModel.get_query(info)  # SQLAlchemy query

        if "skip" in kwargs.keys():
            query = query[kwargs.get("skip") :]

        if "first" in kwargs.keys():
            query = query[: kwargs.get("first")]

        print("--- %s Chapter seconds ---" % (time.time() - start_time))

        return query

    @staticmethod
    def resolve_verses(parent, info, **kwargs):

        if "verseNumber" in kwargs.keys():
            query = models.GitaVerseModel.get_query(info).filter(
                models.GitaVerse.id == kwargs.get("verseNumber")
            )
        elif "limit" in kwargs.keys():
            query = models.GitaVerseModel.get_query(info).limit(kwargs.get("limit"))
        else:
            query = models.GitaVerseModel.get_query(info)

        if "skip" in kwargs.keys():
            query = query[kwargs.get("skip") :]

        if "first" in kwargs.keys():
            query = query[: kwargs.get("first")]

        return query


app = FastAPI()
app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))
