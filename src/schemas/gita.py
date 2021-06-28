from typing import List

from pydantic import BaseModel


class BaseGitaModel(BaseModel):
    id: int

    class Config:
        orm_mode = True


class GitaTranslation(BaseGitaModel):
    description: str
    author_name: str
    language: str


class GitaCommentary(BaseGitaModel):
    description: str
    author_name: str
    language: str


class GitaVerse(BaseGitaModel):
    verse_number: int
    chapter_number: int
    text: str
    translations: List[GitaTranslation] = []
    commentaries: List[GitaCommentary] = []


# class GitaVerse1(BaseGitaModel):
#     title: str
#     verse_order: int
#     verse_number: int
#     chapter_number: int
#     text: str
#     chapter_id: int
#     # translations: List[gitaTranslation] = []
#     # commentaries: List[gitaCommentary] = []


class GitaChapter(BaseGitaModel):
    name: str
    name_transliterated: str
    name_translated: str
    verses_count: int
    chapter_number: int
    name_meaning: str
    chapter_summary: str
