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
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "postgres://fqznwmzmqiceex:738c7ea048798ed49afaa61d99a91273ee3eb42ff704ddaa2ed4c9a5c8dc5d99@ec2-34-251-233-253.eu-west-1.compute.amazonaws.com:5432/d1i3qosk54evtj"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{DB_NAME}')
    #app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://coqbzbhibswkan:5a7468686a129bb417b631d8591d7f6e1874b12fe07abf72fc0bc1651a4d6a0a@ec2-99-80-190-165.eu-west-1.compute.amazonaws.com:5432/dfona0oua7dv66"
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Kilometers

    create_database(app)

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
