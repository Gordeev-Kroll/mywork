# models.py
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text)
    date = Column(Text)
    link = Column(Text)
    text = Column(Text)
    description = Column(Text)

class PersonsToNews(Base):
    __tablename__ = 'persons_to_news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_news = Column(Integer)
    person = Column(Text)

class PlacesToNews(Base):
    __tablename__ = 'places_to_news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_news = Column(Integer)
    places = Column(Text)


DATABASE_URL = 'postgresql://postgres:postgres@localhost/newsdatabase'
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()