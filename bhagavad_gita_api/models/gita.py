from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import UnicodeText

from bhagavad_gita_api.db.base_class import Base


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
