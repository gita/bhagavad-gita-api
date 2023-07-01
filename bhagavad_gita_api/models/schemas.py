from typing import List, Optional

from pydantic import BaseModel


class BaseGitaModel(BaseModel):
    id: int

    class Config:
        orm_mode = True


class GitaTranslation(BaseGitaModel):
    description: str
    author_name: str
    language: str


class GitaTransliteration(BaseGitaModel):

    description: str
    language: str
    verse_id: int
    language_id: int


class GitaCommentary(BaseGitaModel):
    description: str
    author_name: str
    language: str


class GitaVerse(BaseGitaModel):
    verse_number: int
    chapter_number: int
    slug: str
    text: str
    sanskrit_recitation_url: Optional[str]
    transliteration: str
    word_meanings: str
    translations: List[GitaTranslation] = []
    commentaries: List[GitaCommentary] = []
    transliterations: List[GitaTransliteration] = []


class GitaVerseV3(GitaVerse):
    transliterations: Optional[List[GitaTransliteration]]


class GitaVerseBase(BaseGitaModel):
    verse_number: int
    chapter_number: int
    slug: str
    text: str
    transliteration: str
    word_meanings: str


class GitaChapter(BaseGitaModel):
    name: str
    slug: str
    name_transliterated: str
    name_translated: str
    verses_count: int
    chapter_number: int
    name_meaning: str
    chapter_summary: str
    chapter_summary_hindi: str


class VerseOfDay(BaseGitaModel):
    id: int
    verse_order: int


class GitaAuthor(BaseModel):
    author_name: Optional[str]
