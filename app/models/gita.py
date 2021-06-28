from db.session import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import UnicodeText


class GitaCommentary(Base):
    __tablename__ = "gita_commentaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(UnicodeText)
    author_name = Column(String(200))
    language = Column(String(200))
    verse_number = Column(Integer)
    verse_id = Column(Integer, ForeignKey("gita_verses.id"))
    author_id = Column(Integer, ForeignKey("gita_authors.id"))
    language_id = Column(Integer, ForeignKey("gita_languages.id"))


class GitaTranslation(Base):
    __tablename__ = "gita_translations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(UnicodeText)
    author_name = Column(String(200))
    language = Column(String(100))
    verse_number = Column(Integer)
    verse_id = Column(Integer, ForeignKey("gita_verses.id"))
    author_id = Column(Integer, ForeignKey("gita_authors.id"))
    language_id = Column(Integer, ForeignKey("gita_languages.id"))


class GitaLanguage(Base):
    __tablename__ = "gita_languages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String(200))
    translations = relationship(GitaTranslation, lazy="joined")
    commentaries = relationship(GitaCommentary, lazy="joined")


class GitaAuthor(Base):
    __tablename__ = "gita_authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    translations = relationship(GitaTranslation, backref="gitaAuthor")
    commentaries = relationship(GitaCommentary, backref="gitaAuthor")


class GitaVerse(Base):
    __tablename__ = "gita_verses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    verse_number = Column(Integer, index=True)
    chapter_number = Column(Integer, index=True)
    text = Column(UnicodeText, index=True)
    chapter_id = Column(Integer, ForeignKey("gita_chapters.id"))
    translations = relationship(GitaTranslation, backref="gita_verses", lazy="joined")
    commentaries = relationship(GitaCommentary, backref="gita_verses", lazy="joined")


class GitaChapter(Base):
    __tablename__ = "gita_chapters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(UnicodeText, index=True)
    name_transliterated = Column(UnicodeText)
    name_translated = Column(UnicodeText)
    verses_count = Column(Integer)
    chapter_number = Column(Integer)
    name_meaning = Column(UnicodeText)
    chapter_summary = Column(UnicodeText)
    verses = relationship(GitaVerse, backref="gita_chapters", lazy="joined")


# graphql
# class gitaVerseModel(SQLAlchemyObjectType):
#     class Meta:
#         model = GitaVerse
#
#
# class gitaTranslationModel(SQLAlchemyObjectType):
#     class Meta:
#         model = GitaTranslation
#
#
# class gitaCommentryModel(SQLAlchemyObjectType):
#     class Meta:
#         model = GitaCommentary
#
#
# class nestedVersesModel(SQLAlchemyObjectType):
#
#     translations = graphene.List(
#         gitaTranslationModel,
#         authorName=graphene.String(),
#         language=graphene.String(),
#         limit=graphene.Int(),
#         first=graphene.Int(),
#         skip=graphene.Int(),
#     )
#     commentaries = graphene.List(
#         gitaCommentryModel,
#         authorName=graphene.String(),
#         language=graphene.String(),
#         limit=graphene.Int(),
#         first=graphene.Int(),
#         skip=graphene.Int(),
#     )
#
#     class Meta:
#         model = GitaVerse
#         exclude_fields = ("translations", "commentaries")
#
#         # filtering Pending
#
#     def resolve_translations(parent, info, **kwargs):
#
#         if "limit" in kwargs.keys():
#
#             query = (
#                 gitaTranslationModel.get_query(info)
#                 .filter(GitaTranslation.verseNumber == parent.verse_number)
#                 .limit(kwargs.get("limit"))
#             )
#         elif "authorName" in kwargs.keys():
#             query = (
#                 gitaTranslationModel.get_query(info)
#                 .filter(GitaTranslation.authorName == kwargs.get("authorName"))
#                 .filter(GitaTranslation.verseNumber == parent.verse_number)
#             )
#
#         elif "language" in kwargs.keys():
#             query = (
#                 gitaTranslationModel.get_query(info)
#                 .filter(GitaTranslation.lang == kwargs.get("language"))
#                 .filter(GitaTranslation.verseNumber == parent.verse_number)
#             )
#
#         else:
#             query = gitaTranslationModel.get_query(info).filter(
#                 GitaTranslation.verseNumber == parent.verse_number
#             )
#
#         if "skip" in kwargs.keys():
#             query = query[kwargs.get("skip") :]
#
#         if "first" in kwargs.keys():
#             query = query[: kwargs.get("first")]
#
#         return query
#
#     def resolve_commentaries(parent, info, **kwargs):
#         start_time = time.time()
#         if "limit" in kwargs.keys():
#
#             query = (
#                 gitaCommentryModel.get_query(info)
#                 .filter(gitaCommentary.verseNumber == parent.verse_number)
#                 .limit(kwargs.get("limit"))
#             )
#         elif "authorName" in kwargs.keys():
#             query = (
#                 gitaCommentryModel.get_query(info)
#                 .filter(gitaCommentary.authorName == kwargs.get("authorName"))
#                 .filter(gitaCommentary.verseNumber == parent.verse_number)
#             )
#
#         elif "language" in kwargs.keys():
#             query = (
#                 gitaCommentryModel.get_query(info)
#                 .filter(gitaCommentary.lang == kwargs.get("language"))
#                 .filter(gitaCommentary.verseNumber == parent.verse_number)
#             )
#
#         else:
#             query = gitaCommentryModel.get_query(info).filter(
#                 gitaCommentary.verseNumber == parent.verse_number
#             )
#
#         if "skip" in kwargs.keys():
#             query = query[kwargs.get("skip") :]
#
#         if "first" in kwargs.keys():
#             query = query[: kwargs.get("first")]
#
#         print("--- %s commentary seconds ---" % (time.time() - start_time))
#         return query
#
#
# class gitaChapterModel(SQLAlchemyObjectType):
#
#     verses = graphene.List(
#         nestedVersesModel,
#         verseNumber=graphene.Int(),
#         limit=graphene.Int(),
#         first=graphene.Int(),
#         skip=graphene.Int(),
#     )
#
#     class Meta:
#         model = gitaChapter
#         exclude_fields = ("verses",)
#
#     def resolve_verses(parent, info, **kwargs):
#         start_time = time.time()
#
#         if "limit" in kwargs.keys():
#             query = (
#                 gitaVerseModel.get_query(info)
#                 .filter(gitaVerse.chapter_number == parent.chapter_number)
#                 .limit(kwargs.get("limit"))
#             )
#
#         elif "verseNumber" in kwargs.keys():
#             query = (
#                 gitaVerseModel.get_query(info)
#                 .filter(gitaVerse.verse_number == kwargs.get("verseNumber"))
#                 .filter(gitaVerse.chapter_number == parent.chapter_number)
#             )
#
#         else:
#             query = gitaVerseModel.get_query(info).filter(
#                 gitaVerse.chapter_number == parent.chapter_number
#             )
#
#         if "skip" in kwargs.keys():
#             query = query[skip:]
#
#         if "first" in kwargs.keys():
#             query = query[:first]
#
#         print("--- %s Verses seconds ---" % (time.time() - start_time))
#
#         return query
