import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Float
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date
from config import database_setup

database_path = os.environ.get('DATABASE_URL', "postgres://{}:{}@{}/{}".format(database_setup["user_name"], database_setup["password"], database_setup["port"], database_setup["database_name"]))

# database_filename = "database.db"
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():

    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():

    new_actor = (Actor(
        name = 'Sudha',
        gender = 'Female',
        age = 25
        ))

    new_movie = (Movie(
        title = 'Titanic',
        release_date = '1-06-2020'
        ))

    new_stageShow = Stageshow.insert().values(
        Movie_id = new_movie.id,
        Actor_id = new_actor.id,
        show_fee = 500.00
    )

    new_actor.insert()
    new_movie.insert()
    db.session.execute(new_stageShow) 
    db.session.commit()

Stageshow = db.Table('Stageshow', db.Model.metadata,
    db.Column('Movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('Actor_id', db.Integer, db.ForeignKey('actors.id')),
    db.Column('show_fee', db.Float)
)


class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  gender = Column(String)
  age = Column(Integer)

  def __init__(self, name, gender, age):
    self.name = name
    self.gender = gender
    self.age = age

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name' : self.name,
      'gender': self.gender,
      'age': self.age
    }

class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(String)
  actors = db.relationship('Actor', secondary=Stageshow, backref=db.backref('Stageshow', lazy='joined'))

  def __init__(self, title, release_date) :
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title' : self.title,
      'release_date': self.release_date
    }