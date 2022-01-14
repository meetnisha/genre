from sqlalchemy import DateTime, Column, Integer, String
from sqlalchemy.sql import func

from .database import Base

class Genre(Base):
    __tablename__ = "genres"

    trackID = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    genre = Column(String)
    created = Column(DateTime, nullable=False, default=func.now(), index=True)