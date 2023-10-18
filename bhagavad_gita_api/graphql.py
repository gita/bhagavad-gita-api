from graphene import Int, List, ObjectType, String
from graphene_sqlalchemy import SQLAlchemyObjectType

from bhagavad_gita_api.db.session import db_session
from bhagavad_gita_api.models.gita import (
    GitaChapter,
    GitaCommentary,
    GitaTranslation,
    GitaVerse,
)

db = db_session.session_factory()


class GitaTranslationModel(SQLAlchemyObjectType):
    class Meta:
        model = GitaTranslation


class GitaCommentryModel(SQLAlchemyObjectType):
    class Meta:
        model = GitaCommentary


class GitaVerseModel(SQLAlchemyObjectType):
    translations = List(
        GitaTranslationModel,
        authorName=String(),
        language=String(),
        limit=Int(),
        first=Int(),
        skip=Int(),
    )
    commentaries = List(
        GitaCommentryModel,
        authorName=String(),
        language=String(),
        limit=Int(),
        first=Int(),
        skip=Int(),
    )

    class Meta:
        model = GitaVerse
        exclude_fields = ("translations", "commentaries")

        # filtering Pending

    def resolve_translations(parent, info, **kwargs):
        if parent.id:
            verse_id = parent.id
        else:
            verse_id = (
                db.query(GitaVerse)
                .filter(
                    GitaVerse.verse_number == parent.verse_number,
                    GitaVerse.chapter_number == parent.chapter_number,
                )
                .with_entities(
                    GitaVerse.id,
                )
                .first()
            )[0]

        if "limit" in kwargs.keys():
            query = (
                GitaTranslationModel.get_query(info)
                .filter(GitaTranslation.verse_id == verse_id)
                .limit(kwargs.get("limit"))
            )
        elif "authorName" in kwargs.keys():
            query = (
                GitaTranslationModel.get_query(info)
                .filter(GitaTranslation.author_name == kwargs.get("authorName"))
                .filter(GitaTranslation.verse_id == verse_id)
            )

        elif "language" in kwargs.keys():
            query = (
                GitaTranslationModel.get_query(info)
                .filter(GitaTranslation.language == kwargs.get("language"))
                .filter(GitaTranslation.verse_id == verse_id)
            )

        else:
            query = GitaTranslationModel.get_query(info).filter(
                GitaTranslation.verse_id == verse_id
            )

        if "skip" in kwargs.keys():
            query = query[kwargs.get("skip") :]

        if "first" in kwargs.keys():
            query = query[: kwargs.get("first")]

        return query

    def resolve_commentaries(parent, info, **kwargs):
        verse_id = (
            db.query(GitaVerse)
            .filter(
                GitaVerse.verse_number == parent.verse_number,
                GitaVerse.chapter_number == parent.chapter_number,
            )
            .with_entities(
                GitaVerse.id,
            )
            .first()
        )[0]

        if "limit" in kwargs.keys():
            query = (
                GitaCommentryModel.get_query(info)
                .filter(GitaCommentary.verse_id == verse_id)
                .limit(kwargs.get("limit"))
            )
        elif "authorName" in kwargs.keys():
            query = (
                GitaCommentryModel.get_query(info)
                .filter(GitaCommentary.author_name == kwargs.get("authorName"))
                .filter(GitaCommentary.verse_id == verse_id)
            )

        elif "language" in kwargs.keys():
            query = (
                GitaCommentryModel.get_query(info)
                .filter(GitaCommentary.language == kwargs.get("language"))
                .filter(GitaCommentary.verse_id == verse_id)
            )

        else:
            query = GitaCommentryModel.get_query(info).filter(
                GitaCommentary.verse_id == verse_id
            )

        if "skip" in kwargs.keys():
            query = query[kwargs.get("skip") :]

        if "first" in kwargs.keys():
            query = query[: kwargs.get("first")]

        return query


class GitaChapterModel(SQLAlchemyObjectType):
    verses = List(
        GitaVerseModel,
        verse_number=Int(),
        limit=Int(),
        first=Int(),
        skip=Int(),
    )

    class Meta:
        model = GitaChapter
        exclude_fields = ("verses",)

    def resolve_verses(parent, info, **kwargs):
        if "limit" in kwargs.keys():
            query = (
                GitaVerseModel.get_query(info)
                .filter(GitaVerse.chapter_number == parent.chapter_number)
                .limit(kwargs.get("limit"))
            )

        elif "verse_number" in kwargs.keys():
            query = (
                GitaVerseModel.get_query(info)
                .filter(GitaVerse.verse_number == kwargs.get("verse_number"))
                .filter(GitaVerse.chapter_number == parent.chapter_number)
            )

        else:
            query = GitaVerseModel.get_query(info).filter(
                GitaVerse.chapter_number == parent.chapter_number
            )

        if "skip" in kwargs.keys():
            query = query[kwargs.get("skip") :]

        if "first" in kwargs.keys():
            query = query[: kwargs.get("first")]

        return query


class Query(ObjectType):
    chapters = List(
        GitaChapterModel,
        chapter_number=Int(),
        limit=Int(),
        first=Int(),
        skip=Int(),
    )

    verses = List(
        GitaVerseModel,
        verse_number=Int(),
        verse_order=Int(),
        limit=Int(),
        first=Int(),
        skip=Int(),
    )

    @staticmethod
    async def resolve_chapters(self, info, **kwargs):
        if "chapter_number" in kwargs.keys():
            query = GitaChapterModel.get_query(info).filter(
                GitaChapter.chapter_number == kwargs.get("chapter_number")
            )  # SQLAlchemy query
        elif "limit" in kwargs.keys():
            query = GitaChapterModel.get_query(info).limit(kwargs.get("limit"))
        else:
            query = GitaChapterModel.get_query(info)  # SQLAlchemy query

        if "skip" in kwargs.keys():
            query = query[kwargs.get("skip") :]

        if "first" in kwargs.keys():
            query = query[: kwargs.get("first")]

        return query

    @staticmethod
    async def resolve_verses(self, info, **kwargs):
        if "verse_number" in kwargs.keys():
            query = GitaVerseModel.get_query(info).filter(
                GitaVerse.verse_number == kwargs.get("verse_number")
            )
        elif "verse_order" in kwargs.keys():
            query = GitaVerseModel.get_query(info).filter(
                GitaVerse.id == kwargs.get("verse_order")
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
