from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager

# Create an instance of SQLAlchemy
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'darkplace'

    # ************************************************************************ 
    # Configure SQLAlchemy: ********************************

    # 1. Tell flask where the sqlite database is being stored
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # 2. Initialize SQLAlchemy with our Flask app
    db.init_app(app)
    # ************************************************************************


    # ************************************************************************
    # Import and Register the Blueprints: ********************************
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # ************************************************************************

    from .models import User, Note  
    # Importing it here so that we can ensure that models.py runs before initialize and create db
    # Call create_db()

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # Where the user souold be redirected to when the user isn't logged in and login required.
    login_manager.init_app(app) # telling login manager which app we're using

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # This function gets the user object from the user_id.  The user_id is the ID set in the session.


    return app

def create_database(app):
    if not os.path.exists(DB_NAME):  # Check in the current directory
        with app.app_context():
            db.create_all()
        print("Created Database!")
