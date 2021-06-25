from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import  relationship
from sqlalchemy.types import  UnicodeText
from database import Base
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

class gitaCommentary(Base):
    __tablename__ = "gitaCommentary"
    id = Column(Integer, primary_key=True,autoincrement=True)
    description = Column(UnicodeText)
    authorName = Column(String(200))
    lang = Column(String(200))
    verseNumber = Column(Integer)
    verse_id = Column(Integer,ForeignKey('gitaVerse.id'))
    author_id = Column(Integer,ForeignKey("gitaAuthor.id"))
    language_id = Column(Integer,ForeignKey('gitaLanguage.id'))
    

class gitaLanguage(Base):
    __tablename__='gitaLanguage'
    id = Column(Integer, primary_key=True,autoincrement=True)
    language = Column(String(200))
    commentaries = relationship('gitaCommentary')
    translations = relationship("gitaTranslation")


class gitaTranslation(Base):

    __tablename__ = 'gitaTranslation'
    id = Column(Integer, primary_key=True,autoincrement=True)
    description = Column(UnicodeText)
    authorName = Column(String(200))
    lang = Column(String(100))
    verseNumber = Column(Integer)
    verse_id = Column(Integer,ForeignKey('gitaVerse.id'))
    author_id = Column(Integer,ForeignKey('gitaAuthor.id'))
    language_id = Column(Integer,ForeignKey('gitaLanguage.id'))



class gitaAuthor(Base):

    __tablename__ = "gitaAuthor"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(200))
    translations = relationship('gitaTranslation',backref="gitaAuhtor")
    commentaries = relationship('gitaCommentary',backref="gitaAuthor")




class gitaVerse(Base):
    __tablename__ = "gitaVerse"
    id = Column(Integer, primary_key=True,index=True, autoincrement=True)
    externalId = Column(Integer,index=True)
    title = Column(UnicodeText,unique=True,index=True)
    verse_order = Column(Integer,index=True)
    verse_number = Column(Integer,index=True)
    chapter_number = Column(Integer,index=True)
    text = Column(UnicodeText,index=True)
    chapter_id = Column(Integer,ForeignKey('gitaChapter.id'))
    translations = relationship(gitaTranslation,backref="gitaVerse")
    commentaries = relationship(gitaCommentary,backref="gitaVerse")


class gitaChapter(Base):

    __tablename__ = 'gitaChapter'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(UnicodeText,index=True)
    name_transliterated = Column(UnicodeText)
    name_translation = Column(UnicodeText)
    verses_count = Column(Integer)
    chapter_number = Column(Integer)
    name_meaning  = Column(UnicodeText)
    image_name = Column(String)
    chapter_summary = Column(UnicodeText)
    verses = relationship(gitaVerse,backref="gitaChapter")




#graphql


class gitaChapterModel(SQLAlchemyObjectType):
    class Meta:
        model = gitaChapter


class gitaVerseModel(SQLAlchemyObjectType):
    class Meta:
        model = gitaVerse

class gitaTranslationModel(SQLAlchemyObjectType):
    class Meta:
        model = gitaTranslation
        filter_fields = {
            'authorName':['exact','icontains'],
        }


class gitaCommentryModel(SQLAlchemyObjectType):
    class Meta:
        model = gitaCommentary

