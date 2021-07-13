# Sample GraphQL Queries

## 1. Get all chapters with verses, translations and commentaries

```graphql
query {
  allChapters {
    edges {
      node {
        name
        chapterNumber
        nameTranslated
        nameTransliterated
        nameMeaning
        versesCount
        verses {
          edges {
            node {
              verseNumber
              translations {
                edges {
                  node {
                    language
                    description
                  }
                }
              }
              commentaries {
                edges {
                  node {
                    language
                    description
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```
