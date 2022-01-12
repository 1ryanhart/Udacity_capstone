import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Movie
Have title and release year
'''
class Movie(db.Model):
  __tablename__ = 'movie'

  id = Column(db.Integer, primary_key=True)
  title = Column(db.String)
  releaseDate = Column(db.DateTime)

  def __init__(self, title, releaseDate):
    self.title = title
    self.releaseDate = releaseDate

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'releaseDate': self.releaseDate}

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

'''
Actor
Have name, age, gender
'''
class Actor(db.Model):
  __tablename__ = 'actor'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String)
  age = Column(db.Integer)
  gender = Column(db.String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender}

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()
