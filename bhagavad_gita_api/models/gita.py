from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Index
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.types import UnicodeText

from bhagavad_gita_api.db.base_class import Base


class GitaCommentary(Base):
    __tablename__ = "gita_commentaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(UnicodeText)
    author_name = Column(String(200))
    language = Column(String(200))
    verse_id = Column(Integer, ForeignKey("gita_verses.id"))
    author_id = Column(Integer, ForeignKey("gita_authors.id"))
    language_id = Column(Integer, ForeignKey("gita_languages.id"))

    __table_args__ = (Index("ix_commentary", "author_name", "language", "verse_id"),)


class GitaTranslation(Base):
    __tablename__ = "gita_translations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(UnicodeText)
    author_name = Column(String(200))
    language = Column(String(100))
    verse_id = Column(Integer, ForeignKey("gita_verses.id"))
    author_id = Column(Integer, ForeignKey("gita_authors.id"))
    language_id = Column(Integer, ForeignKey("gita_languages.id"))

    __table_args__ = (Index("ix_translation", "author_name", "language", "verse_id"),)


class GitaTransliteration(Base):
    __tablename__ = "gita_transliterations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(UnicodeText)
    language = Column(String(100))
    verse_id = Column(Integer, ForeignKey("gita_verses.id"))
    language_id = Column(Integer, ForeignKey("gita_languages.id"))

    __table_args__ = (Index("ix_transliteration", "language", "verse_id"),)


class GitaLanguage(Base):
    __tablename__ = "gita_languages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String(200))
    translations = relationship(GitaTranslation, lazy="joined")
    commentaries = relationship(GitaCommentary, lazy="joined")

    __table_args__ = (Index("ix_language", "language"),)


class GitaAuthor(Base):
    __tablename__ = "gita_authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    translations = relationship(GitaTranslation, backref="gitaAuthor")
    commentaries = relationship(GitaCommentary, backref="gitaAuthor")

    __table_args__ = (Index("ix_author", "name"),)


class GitaVerse(Base):
    __tablename__ = "gita_verses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(UnicodeText)
    verse_number = Column(Integer)
    chapter_number = Column(Integer)
    text = Column(UnicodeText)
    sanskrit_recitation_url = Column(UnicodeText)
    transliteration = Column(UnicodeText)
    word_meanings = Column(UnicodeText)
    chapter_id = Column(Integer, ForeignKey("gita_chapters.id"))
    translations = relationship(GitaTranslation, backref="gita_verses", lazy="joined")
    commentaries = relationship(GitaCommentary, backref="gita_verses", lazy="joined")
    transliterations = relationship(
        GitaTransliteration, backref="gita_verses", lazy="joined"
    )

    __table_args__ = (Index("ix_verse", "chapter_number", "verse_number", "slug"),)


class GitaChapter(Base):
    __tablename__ = "gita_chapters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(UnicodeText)
    slug = Column(UnicodeText)
    name_transliterated = Column(UnicodeText)
    name_translated = Column(UnicodeText)
    verses_count = Column(Integer)
    chapter_number = Column(Integer)
    name_meaning = Column(UnicodeText)
    chapter_summary = Column(UnicodeText)
    verses = relationship(GitaVerse, backref="gita_chapters", lazy="joined")

    __table_args__ = (Index("ix_chapter", "chapter_number", "slug"),)


class VerseOfDay(Base):
    __tablename__ = "verse_of_the_day"

    id = Column(Integer, primary_key=True, autoincrement=True)
    verse_order = Column(Integer)
    date = Column(Date)
