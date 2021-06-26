from typing import List, Optional
from pydantic import BaseModel


class gitaTranslation(BaseModel):
    id: int
    description: str
    authorName: str
    lang: str
    verseNumber: int
    verse_id: int
    author_id: int
    language_id: int
    class Config:
        orm_mode = True

class gitaCommentary(BaseModel):
    id: int
    description: str
    authorName: str
    lang: str
    verseNumber: int
    verse_id: int
    author_id: int
    language_id: int
    class Config:
        orm_mode = True

class gitaVerse(BaseModel):
    id: int
    externalId: int
    title: str
    verse_order: int
    verse_number: int
    chapter_number: int
    text: str
    chapter_id: int
    translations: List[gitaTranslation] = []
    commentaries: List[gitaCommentary] = []
    class Config:
        orm_mode = True

class gitaVerse1(BaseModel):
    id: int
    externalId: int
    title: str
    verse_order: int
    verse_number: int
    chapter_number: int
    text: str
    chapter_id: int
    # translations: List[gitaTranslation] = []
    # commentaries: List[gitaCommentary] = []
    class Config:
        orm_mode = True
        
class gitaChapter(BaseModel):
    id: int
    name: str
    name_transliterated: str
    name_translation: str
    verses_count: int
    chapter_number: int
    name_meaning: str
    image_name: str
    chapter_summary: str
    class Config:
        orm_mode = True



    
