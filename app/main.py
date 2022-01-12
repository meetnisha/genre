import models
from fastapi import FastAPI, Request, Depends, BackgroundTasks, File, UploadFile
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from pydantic import BaseModel 
from models import Genre
from sqlalchemy.orm import Session
import csv 
import codecs
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

class GenreRequest(BaseModel):
    symbol: str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"title": "Hello Coder"}

""" @app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    genres = db.query(Genre)    
    genres = genres.all()

    return templates.TemplateResponse("home.html", {
        "request": request, 
        "genres": genres
    })


def classify_genres(df: object):
    pass

@app.post("/upload")
async def find_genre(background_tasks: BackgroundTasks, csv_file: UploadFile = File(...), db: Session = Depends(get_db)):
    #Get the list of test.csv into an data frame object 
    # and call classify function
    # Return id and genre as part of the classification
    # Persist it to the DB

    df = csv.reader(codecs.iterdecode(csv_file.file,'utf-8'))
 
    genre = Genre()
    genre.id = "123"
    genre.genre = "Rap"
    db.add(genre)
    db.commit()

    background_tasks.add_task(classify_genres, df)

    return {
        "code": "success",
        "message": "genre was added to the database"
    } """