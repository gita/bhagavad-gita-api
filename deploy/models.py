from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import  relationship
from sqlalchemy.types import  UnicodeText
from database import Base
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet
import graphene
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
class gitaVerseModel(SQLAlchemyObjectType):
    class Meta:
        model = gitaVerse


class gitaTranslationModel(SQLAlchemyObjectType):
    class Meta:
        model = gitaTranslation
        


class gitaCommentryModel(SQLAlchemyObjectType):
    class Meta:
        model = gitaCommentary



class nestedVersesModel(SQLAlchemyObjectType):

    translations = graphene.List(
        gitaTranslationModel,
        authorName = graphene.String(),
        language = graphene.String(),
        limit = graphene.Int(),
        first = graphene.Int(),
        skip = graphene.Int()
    )
    commentaries = graphene.List(
        gitaCommentryModel,
        authorName = graphene.String(),
        language = graphene.String(),
        limit = graphene.Int(),
        first = graphene.Int(),
        skip = graphene.Int()

    )
    class Meta:
        model = gitaVerse
        exclude_fields = ('translations','commentaries')

        #filtering Pending
    def resolve_translations(parent,info,**kwargs):

       
        if "limit" in kwargs.keys():
            
            query = gitaTranslationModel.get_query(info).filter(gitaTranslation.verseNumber == parent.verse_number).limit(kwargs.get('limit'))
        elif 'authorName' in kwargs.keys():
            query = gitaTranslationModel.get_query(info).filter(gitaTranslation.authorName == kwargs.get('authorName')).filter(gitaTranslation.verseNumber == parent.verse_number)
        
        elif "language" in kwargs.keys():
            query = gitaTranslationModel.get_query(info).filter(gitaTranslation.lang == kwargs.get('language')).filter(gitaTranslation.verseNumber == parent.verse_number)
            
        else:
            query = gitaTranslationModel.get_query(info).filter(gitaTranslation.verseNumber == parent.verse_number)

        if "skip" in kwargs.keys():
            query = query[kwargs.ger('skip'):]

        if 'first' in kwargs.keys():
            query = query[:kwargs.get('first')]

        return query

    def resolve_commentaries(parent,info,**kwargs):

        if "limit" in kwargs.keys():
            
            query = gitaCommentryModel.get_query(info).filter(gitaCommentary.verseNumber == parent.verse_number).limit(kwargs.get('limit'))
        elif 'authorName' in kwargs.keys():
            query = gitaCommentryModel.get_query(info).filter(gitaCommentary.authorName == kwargs.get('authorName')).filter(gitaCommentary.verseNumber == parent.verse_number)
        
        elif "language" in kwargs.keys():
            query = gitaCommentryModel.get_query(info).filter(gitaCommentary.lang == kwargs.get('language')).filter(gitaCommentary.verseNumber == parent.verse_number)
            
        else:
            query = gitaCommentryModel.get_query(info).filter(gitaCommentary.verseNumber == parent.verse_number)
        
        if "skip" in kwargs.keys():
            query = query[kwargs.ger('skip'):]

        if 'first' in kwargs.keys():
            query = query[:kwargs.get('first')]

        return query



class gitaChapterModel(SQLAlchemyObjectType):

    verses = graphene.List(
        nestedVersesModel,
        verseNumber = graphene.Int(),
        limit = graphene.Int(),
        first = graphene.Int(),
        skip = graphene.Int()
        )
    class Meta:
        model = gitaChapter
        exclude_fields = ('verses',)

    def resolve_verses(parent,info,**kwargs):
        
        if "limit" in kwargs.keys():
            query = gitaVerseModel.get_query(info).filter(gitaVerse.chapter_number == parent.chapter_number).limit(kwargs.get('limit'))

        elif "verseNumber" in kwargs.keys():
            query = gitaVerseModel.get_query(info).filter(gitaVerse.verse_number == kwargs.get('verseNumber')).filter(gitaVerse.chapter_number == parent.chapter_number)

        else:
            query = gitaVerseModel.get_query(info).filter(gitaVerse.chapter_number == parent.chapter_number)
        
        if "skip" in kwargs.keys():
            query = query[skip:]

        if 'first' in kwargs.keys():
            query = query[:first]

        return query
        



