# Sample GraphQL Queries

## 1. Get all chapters with verses, translations and commentaries

```graphql
query{
  chapters {
    name
    chapterNumber
    nameTranslated
    versesCount
    verses {
      verseNumber
      translations {
        language
        description
      }
      commentaries {
        language
        description
      }
    }
  }
}
```
