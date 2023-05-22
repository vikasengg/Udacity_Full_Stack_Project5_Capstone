import os
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, create_engine
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

import json

db = SQLAlchemy()

# Setting up DB config using path
def setup_db(app,database_path=DATABASE_URI):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Creating DB if it doesn't already exist
    if not database_exists(database_path):
        create_database(database_path)
    
    db.app = app
    db.init_app(app)

def setup_migrations(app):
    migrate = Migrate(app, db)

# DROP and CREATE tables for test
def create_tables_for_test():
    db.drop_all()
    db.create_all()

'''
Movie Class
'''
class Movie(db.Model):
    __tablename__ = 'movies'
    # Autoincrementing, unique primary key
    id = Column(db.Integer(),primary_key=True)
    # String Movie Name
    name = Column(db.String())
    # Date Time Movie Release date 
    release_date= Column(db.Date())

    # Self initialize the variables 
    def __init__(self, name, release_date):
        self.name = name
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def serialized_movie(self):
        return {
                "id": self.id,
                "name": self.name,
                "release_date": self.release_date.isoformat()
                }

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'release_date': self.release_date
            }
    
'''
Actors Class
'''
class Actor(db.Model):

    __tablename__ = 'actors'

    # Autoincrementing, unique primary key
    id = Column(db.Integer(), primary_key=True)
    # String Actor Name
    name = Column(db.String())
    # Integer Actor's Age
    age = Column(db.Integer())
    # Integer Actor's Gender
    gender = Column(db.String())

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialized_actor(self):
        return (
            {"id": self.id,
             "name": self.name,
             "age": self.age,
             "gender": self.gender}
        )

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }