from datetime import datetime
from . import models
from fastapi import FastAPI, Request, Depends, BackgroundTasks, File, UploadFile
from fastapi.templating import Jinja2Templates
from .database import conn, engine
from pydantic import BaseModel 
from .models import Genre
from sqlalchemy.orm import Session
import pandas as pd
import io
import datetime
app = FastAPI()
from pathlib import Path

models.Base.metadata.create_all(bind=engine)

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

#templates = Jinja2Templates(directory="templates")

class GenreRequest(BaseModel):
    symbol: str


def get_db():
    try:
        db = conn()
        yield db
    finally:
        db.close()

""" @app.get("/")
def index():
    return {"title": "Hello Coder"} """

@app.get("/")
def home(request: Request):
    query = "SELECT * FROM genres"
    cur = conn.cursor()
    cur.execute(query)
    genres = cur.fetchall()

    """ genres = conn.query(Genre)    
    genres = genres.all() """
    
    return templates.TemplateResponse("home.html", {
        "request": request, 
        "genres": genres
    })


def classify_genres(df: object, current: object):
    # assign data of lists.  
    data = {'trackID': [20, 21, 19, 18], 'title': ['Tom', 'Joseph', 'Krish', 'John'],
    'genre': ['classic', 'rock', 'sufi', 'romantic'], 'created': [current, current, current, current]}  
    
    # Create DataFrame  
    df_cls = pd.DataFrame(data)  
    return df_cls

@app.post("/upload/")
async def form_post(excel: UploadFile = File(...)):
    """Uploads the file and processes it in Pandas"""
    contents = await excel.read()
    test_data = io.BytesIO(contents)
    df = pd.read_csv(test_data, sep=";")
    current = datetime.datetime.now()
    df_cls = classify_genres(df,current)
    df_cls.to_sql("genres", con=conn, if_exists='replace')

    # genre = Genre()
    # genre.id = "123"
    # genre.genre = "Rap"
    # db.add(genre)
    # db.commit()        

    #background_tasks.add_task(classify_genres, df)
    query = "SELECT * FROM genres WHERE created={} and ".format(current)
    cur = conn.cursor()
    cur.execute(query)
    results = await cur.fetchall()

    
    #results = await conn.fetch_all(query=query)

    return  results

""" @app.post("/upload")
async def find_genre(background_tasks: BackgroundTasks, csv_file: UploadFile = File(...), db: Session = Depends(get_db)):
    #Get the list of test.csv into an data frame object 
    # and call classify function
    # Return id and genre as part of the classification
    # Persist it to the DB
    print('HIIII')
    print(csv_file.file)
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