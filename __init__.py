from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__) #to look for static files etc
app.config['SECRET_KEY'] = '7748664f010afab4160bad2d7b7bfcd4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# /// -> same path
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) 
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.message_category = 'info'


from flaskblog import routes