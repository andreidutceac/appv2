from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os
import psycopg2

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    #DATABASE_URL = os.environ['DATABASE_URL']
    #conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SECRET_KEY'] = '8893343f4ef43'
    DATABASE_URL1 = "postgresql://xmsgovjuxnlmfl:c5ab21eb4039b171a3d3b2c479b10d2ad783cbc91d97b2eef1a71cee7bcbf4cb@ec2-34-254-138-204.eu-west-1.compute.amazonaws.com:5432/ddfqfc99vrkd6r"
    # DATABASE_URL1.encode('utf-8')
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL1
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", f'sqlite:///{DB_NAME}').replace("postgres://", "postgresql://", 1)
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", f'sqlite:///{DB_NAME}')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://coqbzbhibswkan:5a7468686a129bb417b631d8591d7f6e1874b12fe07abf72fc0bc1651a4d6a0a@ec2-99-80-190-165.eu-west-1.compute.amazonaws.com:5432/dfona0oua7dv66"
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Kilometers

    # create only when you want to modify the base
    # create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
    # db.create_all(app=app)
