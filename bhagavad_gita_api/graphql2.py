import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from bhagavad_gita_api.db.session import db_session
from bhagavad_gita_api.models.gita import GitaAuthor as GitaAuthorModel
from bhagavad_gita_api.models.gita import GitaChapter as GitaChapterModel
from bhagavad_gita_api.models.gita import GitaCommentary as GitaCommentaryModel
from bhagavad_gita_api.models.gita import GitaLanguage as GitaLanguageModel
from bhagavad_gita_api.models.gita import GitaTranslation as GitaTranslationModel
from bhagavad_gita_api.models.gita import GitaVerse as GitaVerseModel

db = db_session.session_factory()


class GitaLanguage(SQLAlchemyObjectType):
    class Meta:
        model = GitaLanguageModel
        interfaces = (relay.Node,)


class GitaAuthor(SQLAlchemyObjectType):
    class Meta:
        model = GitaAuthorModel
        interfaces = (relay.Node,)


class GitaTranslation(SQLAlchemyObjectType):
    class Meta:
        model = GitaTranslationModel
        interfaces = (relay.Node,)


class GitaCommentary(SQLAlchemyObjectType):
    class Meta:
        model = GitaCommentaryModel
        interfaces = (relay.Node,)


class GitaChapter(SQLAlchemyObjectType):
    class Meta:
        model = GitaChapterModel
        interfaces = (relay.Node,)


class GitaVerse(SQLAlchemyObjectType):
    class Meta:
        model = GitaVerseModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_chapters = SQLAlchemyConnectionField(GitaChapter.connection)
    all_verses = SQLAlchemyConnectionField(GitaVerse.connection)
    all_translations = SQLAlchemyConnectionField(GitaTranslation.connection)
    all_commentaries = SQLAlchemyConnectionField(GitaCommentary.connection)
    all_languages = SQLAlchemyConnectionField(GitaLanguage.connection)
    all_authors = SQLAlchemyConnectionField(GitaAuthor.connection)

    chapters = graphene.List(GitaChapter)
    verses = graphene.List(GitaVerse)
    translations = graphene.List(GitaTranslation)
    commentaries = graphene.List(GitaCommentary)
    languages = graphene.List(GitaLanguage)
    authors = graphene.List(GitaAuthor)

    chapter = graphene.Node.Field(GitaChapter)
    verse = graphene.Node.Field(GitaVerse)
    translation = graphene.Node.Field(GitaTranslation)
    commentary = graphene.Node.Field(GitaCommentary)
    language = graphene.Node.Field(GitaLanguage)
    author = graphene.Node.Field(GitaAuthor)

    def resolve_chapters(self, info):
        return GitaChapterModel.query.all()

    def resolve_verses(self, info):
        return GitaVerseModel.query.all()

    def resolve_translations(self, info):
        return GitaTranslationModel.query.all()

    def resolve_commentaries(self, info):
        return GitaCommentaryModel.query.all()

    def resolve_languages(self, info):
        return GitaLanguageModel.query.all()

    def resolve_authors(self, info):
        return GitaAuthorModel.query.all()
