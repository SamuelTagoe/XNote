# Gonna have db model for both users and notes.
# A db model is a blueprint for an obj that is going to be stored in a db

from . import db                        # Import db from our current package which is __init__.
from flask_login import UserMixin       # To give our user object things specific to our flask_login module
from sqlalchemy import func             # This would allow SQLAlchemy to specify the date for us automatically (Func gets the current date and time)

# Every Class should Inherit from db.Model

# set up a note obj
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # Define the relationship between the Note Obj and User obj 
    # This is done by a ForeignKey relationship, the foreign key is a key on one of the db tables
    # that references an ID to another db column
    # So in this instance, for every single note, we need to store the ID of the user who created this note in the database
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # So a valid id has to be passed, one to many relationship(One user can have many notes)

# Instance of UserMixin and defining user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    # Everytime we create a note add into this user note's relationship that note id
    # this relationship field will be really be a list that will store all of the different notes
    notes = db.relationship('Note')
