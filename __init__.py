################################################################
# Importing my packages

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

##################################################################

## Initializing database for usage in later models ##
db = SQLAlchemy()

###################################################################

## creating our app run functions ##

def create_app():
    app = Flask(__name__) ## Creates the flask instance, __name__ is the name of the module of the current python module
    app.config['SECRET_KEY'] = 'cMVyvhYWQW72ou9uHV^O@(!PnkVJ@^!I&^!Inckdbnl(UPu28h8'  ## This used by flask and some extensions to keep data safe
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  ## it is the path where the SQLite database file will be saved
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # deactivate Flask-SQLAlchemy track modifications
    db.init_app(app)  ## initialize sqlite database

####################################################################

    #The login manager contains the code that lets your application and Flask-Login work together
    login_manager = LoginManager() # Loads the LoginManager module
    login_manager.login_view = 'auth_login' 

####################################################################

    login_manager.init_app(app) #Define the app function as rhe initiative of the login manager
    from models import User # Imports the User Function and data from the models.py Folder

####################################################################

    @login_manager.user_loader
    def load_user(user_id): # Creates a functio with an automatic input of user_id
        return User.query.get(int(user_id)) # Returns the details of the user in the database such as Name, Id and so on

####################################################################

    from auth import auth as auth_blueprint 
    app.register_blueprint(auth_blueprint) # Creates a flask auth_blueprint which is just basically run the code in auth.py file in the folder 

####################################################################

    from main import main as main_blueprint # Import main.py but change the name to main_blueprint instead
    app.register_blueprint(main_blueprint) # Creates a flask main_blueprint which is just basically run the code in main.py
    return app  # When everything above has been done with no issues then return the values, data just basically re