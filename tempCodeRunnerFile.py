@app.get("/chapters/", response_model=List[schemas.gitChapter])
# def read_chapters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     chapters = crud.get_chapters(db, skip=skip, limit=limit)
#     return chapters
