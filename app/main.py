from pathlib import Path
from datetime import datetime
from .database import models
from fastapi import FastAPI, Request, Depends, BackgroundTasks, File, UploadFile
from fastapi.templating import Jinja2Templates
from .database.database import SessionLocal, engine
from pydantic import BaseModel
from .database.models import Genre
from .classification import classify
from sqlalchemy import select
from sqlalchemy.orm import Session
import pandas as pd
import io
from starlette.responses import RedirectResponse

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

#templates = Jinja2Templates(directory="templates")


class GenreRequest(BaseModel):
    symbol: str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)) -> object:
    genres = db.query(Genre)
    genres = genres.all()
    #print(genres)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "genres": genres
    })


@app.post("/upload/")
async def form_post(request: Request, excel: UploadFile = File(...), db: Session = Depends(get_db)
                    ) -> object:
    """Uploads the file and processes it in Pandas"""
    contents = await excel.read()
    test_data = io.BytesIO(contents)    
    df = pd.read_csv(test_data)
    current = datetime.now()
    print('main', len(df.columns))
    df_cls = classify.classify_genres(df, current)

    # with SessionLocal.begin() as session:
    #db.bulk_insert_mappings(Genre, df_cls)
    objects = []
    for idx, item in df_cls.iterrows():
        one_object = Genre(
            trackID=item[0], title=item[1], genre=item[2], created=item[3])
        objects.append(one_object)

    try:
        db.bulk_save_objects(objects)
        db.commit()
    except:
        return {
            "code": "error",
            "message": "Some or all trackIds have been classified already."
        }

    """ # query from a class
    statement = select(Genre).filter_by(created=current)

    # list of first element of each row (i.e. Genre objects)
    results = db.execute(statement).scalars().all()
    message = {"code": "success",
            "message": "genre was added to the database"}
    print(message) """


    return RedirectResponse(url="/", status_code=302)