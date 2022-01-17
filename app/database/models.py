from sqlalchemy import DateTime, Column, Integer, String
from sqlalchemy.sql import func

from .database import Base

class Tracks(Base):
    __tablename__ = "tracks"

    trackID = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    genre = Column(String)
    created = Column(DateTime, nullable=False, default=func.now(), index=True)

class Genres(Base):
    __tablename__ = "genres"

    genreID = Column(Integer, primary_key=True, index=True)
    genreName = Column(String)