import time

import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from bhagavad_gita_api import models
from bhagavad_gita_api.models.gita import (
    GitaTranslation,
    GitaCommentary,
    GitaVerse,
    GitaChapter,
)

from bhagavad_gita_api.db.session import db_session

db = db_session.session_factory()


class GitaTranslationModel(SQLAlchemyObjectType):
    class Meta:
        model = GitaTranslation


class GitaCommentryModel(SQLAlchemyObjectType):
    class Meta:
        model = GitaCommentary


class GitaVerseModel(SQLAlchemyObjectType):
    translations = graphene.List(
        GitaTranslationModel,
        authorName=graphene.String(),
        language=graphene.String(),
        limit=graphene.Int(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    commentaries = graphene.List(
        GitaCommentryModel,
        authorName=graphene.String(),
        language=graphene.String(),
        limit=graphene.Int(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    class Meta:
        model = GitaVerse
        exclude_fields = ("translations", "commentaries")

        # filtering Pending

    def resolve_translations(parent, info, **kwargs):

        if "limit" in kwargs.keys():

            query = (
                GitaTranslationModel.get_query(info)
                .filter(GitaTranslation.verse_id == parent.verse_number)
                .limit(kwargs.get("limit"))
            )
        elif "authorName" in kwargs.keys():
            query = (
                GitaTranslationModel.get_query(info)
                .filter(GitaTranslation.authorName == kwargs.get("authorName"))
                .filter(GitaTranslation.verse_id == parent.verse_number)
            )

        elif "language" in kwargs.keys():
            query = (
                GitaTranslationModel.get_query(info)
                .filter(GitaTranslation.lang == kwargs.get("language"))
                .filter(GitaTranslation.verse_id == parent.verse_number)
            )

        else:
            query = GitaTranslationModel.get_query(info).filter(
                GitaTranslation.verse_id == parent.verse_number
            )

        if "skip" in kwargs.keys():
            query = query[kwargs.get("skip") :]

        if "first" in kwargs.keys():
            query = query[: kwargs.get("first")]

        return query

    def resolve_commentaries(parent, info, **kwargs):
        start_time = time.time()
        if "limit" in kwargs.keys():

            query = (
                GitaCommentryModel.get_query(info)
                .filter(GitaCommentary.verse_id == parent.verse_number)
                .limit(kwargs.get("limit"))
            )
        elif "authorName" in kwargs.keys():
            query = (
                GitaCommentryModel.get_query(info)
                .filter(GitaCommentary.authorName == kwargs.get("authorName"))
                .filter(GitaCommentary.verse_id == parent.verse_number)
            )

        elif "language" in kwargs.keys():
            query = (
                GitaCommentryModel.get_query(info)
                .filter(GitaCommentary.lang == kwargs.get("language"))
                .filter(GitaCommentary.verse_id == parent.verse_number)
            )

        else:
            query = GitaCommentryModel.get_query(info).filter(
                GitaCommentary.verse_id == parent.verse_number
            )

        if "skip" in kwargs.keys():
            query = query[kwargs.get("skip") :]

        if "first" in kwargs.keys():
            query = query[: kwargs.get("first")]

        print("--- %s commentary seconds ---" % (time.time() - start_time))
        return query


class nestedVersesModel(SQLAlchemyObjectType):

    translations = graphene.List(
        GitaTranslationModel,
        authorName=graphene.String(),
        language=graphene.String(),
        limit=graphene.Int(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    commentaries = graphene.List(
        GitaCommentryModel,
        authorName=graphene.String(),
        language=graphene.String(),
        limit=graphene.Int(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    class Meta:
        model = GitaVerse
        exclude_fields = ("translations", "commentaries")

        # filtering Pending

    def resolve_translations(parent, info, **kwargs):

        if "limit" in kwargs.keys():

            query = (
                GitaTranslationModel.get_query(info)
                .filter(GitaTranslation.verse_id == parent.verse_number)
                .limit(kwargs.get("limit"))
            )
        elif "authorName" in kwargs.keys():
            query = (
                GitaTranslationModel.get_query(info)
                .filter(GitaTranslation.authorName == kwargs.get("authorName"))
                .filter(GitaTranslation.verse_id == parent.verse_number)
            )

        elif "language" in kwargs.keys():
            query = (
                GitaTranslationModel.get_query(info)
                .filter(GitaTranslation.lang == kwargs.get("language"))
                .filter(GitaTranslation.verse_id == parent.verse_number)
            )

        else:
            query = GitaTranslationModel.get_query(info).filter(
                GitaTranslation.verse_id == parent.verse_number
            )

        if "skip" in kwargs.keys():
            query = query[kwargs.get("skip") :]

        if "first" in kwargs.keys():
            query = query[: kwargs.get("first")]

        return query

    def resolve_commentaries(parent, info, **kwargs):
        start_time = time.time()
        if "limit" in kwargs.keys():

            query = (
                GitaCommentryModel.get_query(info)
                .filter(GitaCommentary.verse_id == parent.verse_number)
                .limit(kwargs.get("limit"))
            )
        elif "authorName" in kwargs.keys():
            query = (
                GitaCommentryModel.get_query(info)
                .filter(GitaCommentary.authorName == kwargs.get("authorName"))
                .filter(GitaCommentary.verse_id == parent.verse_number)
            )

        elif "language" in kwargs.keys():
            query = (
                GitaCommentryModel.get_query(info)
                .filter(GitaCommentary.lang == kwargs.get("language"))
                .filter(GitaCommentary.verse_id == parent.verse_number)
            )

        else:
            query = GitaCommentryModel.get_query(info).filter(
                GitaCommentary.verse_id == parent.verse_number
            )

        if "skip" in kwargs.keys():
            query = query[kwargs.get("skip") :]

        if "first" in kwargs.keys():
            query = query[: kwargs.get("first")]

        print("--- %s commentary seconds ---" % (time.time() - start_time))
        return query


class GitaChapterModel(SQLAlchemyObjectType):

    verses = graphene.List(
        nestedVersesModel,
        verse_id=graphene.Int(),
        limit=graphene.Int(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    class Meta:
        model = GitaChapter
        exclude_fields = ("verses",)

    def resolve_verses(parent, info, **kwargs):
        start_time = time.time()

        if "limit" in kwargs.keys():
            query = (
                GitaVerseModel.get_query(info)
                .filter(GitaVerse.chapter_number == parent.chapter_number)
                .limit(kwargs.get("limit"))
            )

        elif "verse_id" in kwargs.keys():
            query = (
                GitaVerseModel.get_query(info)
                .filter(GitaVerse.verse_number == kwargs.get("verse_id"))
                .filter(GitaVerse.chapter_number == parent.chapter_number)
            )

        else:
            query = GitaVerseModel.get_query(info).filter(
                GitaVerse.chapter_number == parent.chapter_number
            )

        if "skip" in kwargs.keys():
            query = query[skip:]

        if "first" in kwargs.keys():
            query = query[:first]

        print("--- %s Verses seconds ---" % (time.time() - start_time))

        return query


class Query(graphene.ObjectType):
    chapters = graphene.List(
        GitaChapterModel,
        chapterNumber=graphene.Int(),
        limit=graphene.Int(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    verses = graphene.List(
        GitaVerseModel,
        verse_id=graphene.Int(),
        limit=graphene.Int(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    @staticmethod
    def resolve_chapters(parent, info, **kwargs):
        start_time = time.time()

        if "chapterNumber" in kwargs.keys():
            query = GitaChapterModel.get_query(info).filter(
                GitaChapter.chapter_number == kwargs.get("chapterNumber")
            )  # SQLAlchemy query
        elif "limit" in kwargs.keys():
            query = GitaChapterModel.get_query(info).limit(kwargs.get("limit"))
        else:

            query = GitaChapterModel.get_query(info)  # SQLAlchemy query

        if "skip" in kwargs.keys():
            query = query[kwargs.get("skip") :]

        if "first" in kwargs.keys():
            query = query[: kwargs.get("first")]

        print("--- %s Chapter seconds ---" % (time.time() - start_time))

        return query

    @staticmethod
    def resolve_verses(parent, info, **kwargs):

        if "verse_id" in kwargs.keys():
            query = GitaVerseModel.get_query(info).filter(
                GitaVerse.id == kwargs.get("verse_id")
            )
        elif "limit" in kwargs.keys():
            query = GitaVerseModel.get_query(info).limit(kwargs.get("limit"))
        else:
            query = GitaVerseModel.get_query(info)

        if "skip" in kwargs.keys():
            query = query[kwargs.get("skip") :]

        if "first" in kwargs.keys():
            query = query[: kwargs.get("first")]

        return query
