from sqlalchemy import engine
from fastapi import FastAPI,Request
from sqlalchemy.orm import Session
import models
from database import SessionLocal,engine
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)