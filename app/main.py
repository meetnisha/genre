from pathlib import Path
from datetime import datetime
from .database import models
from fastapi import FastAPI, Request, Depends, BackgroundTasks, File, UploadFile
from fastapi.templating import Jinja2Templates
from .database.database import SessionLocal, engine
from pydantic import BaseModel
from .database.models import Genres, Tracks
from .classification import classify
from sqlalchemy import select
from sqlalchemy.orm import Session
import pandas as pd
import io
from starlette.responses import RedirectResponse
import os
from typing import Optional

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

#templates = Jinja2Templates(directory="templates")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)) -> object:
    tracks = db.query(Tracks)
    tracks = tracks.all()

    return templates.TemplateResponse("home.html", {
        "request": request,
        "tracks": tracks
    })


@app.post("/upload/")
async def form_post(excel: UploadFile = File(...), db: Session = Depends(get_db)
                    ) -> object:
    """Uploads the file and processes it in Pandas"""
    contents = await excel.read()
    test_data = io.BytesIO(contents)    
    df = pd.read_csv(test_data)
    current = datetime.now()
    df_cls, new_genres = classify.classify_genres(df, current, CURRENT_FOLDER)

    # with SessionLocal.begin() as session:
    #db.bulk_insert_mappings(Genre, df_cls)
    objTracks = []
    for idx, item in df_cls.iterrows():
        one_object = Tracks(
            trackID=item[0], title=item[1], genre=item[2], created=item[3])
        objTracks.append(one_object)

    try:
        db.bulk_save_objects(objTracks)
        db.commit()
    except:
        return {
            "code": "error",
            "message": "Some or all trackIds have been classified already."
        }

    objGenres = []
    for key in new_genres:
        one_object = Genres(
            genreID=key, genreName=new_genres[key])
        objGenres.append(one_object)
    try:
        db.bulk_save_objects(objGenres)
        db.commit()
    except:
        return {
            "code": "error",
            "message": "All genreIds have been added already."
        }

    return RedirectResponse(url="/", status_code=302)

@app.get("/search/")
async def home(request: Request, db: Session = Depends(get_db)) -> object:
    genre_filter = request.query_params.get('filter', None)
    print('genre_filter', genre_filter)
    genres = db.query(Genres)
    genres = genres.all()
    if genre_filter == None or genre_filter == '':        
        tracks = db.query(Tracks)
        tracks = tracks.all()
    else:        
        tracks = search_track(genre_filter, db=db)
    
    """ dropdownChoices = {}
    dropdownChoices["Select Genre"] = "-1"
    for item in genres:
        if item.genreName not in dropdownChoices:
            dropdownChoices[item.genreName] = item.genreID """

    return templates.TemplateResponse("search.html", {
        "request": request,
        "tracks": tracks, 
        "genres": genres
    })

def search_track(genre_filter: str, db: Session):
    genres = db.query(Genres).filter(Genres.genreID == genre_filter).first()
    if genres != None:
        tracks = db.query(Tracks).filter(Tracks.genre == genres.genreName).all()
        if tracks != None:
            return tracks
        else:
            return {
                "code": "Warning",
                "message": "No tracks found for this genre."
            }
    else:
        return {
            "code": "error",
            "message": "Requested Genre doesnot exist."
        }
    
