from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    #date = db.Column(db.DateTime, default=func.now())
    date = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Kilometers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #date = db.Column(db.DateTime, default=func.now())
    date = db.Column(db.String(20))
    km = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #date = db.Column(db.DateTime, default=func.now())
    date = db.Column(db.String(20))
    pages = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    km = db.relationship('Kilometers')
    pages = db.relationship('Reading')
    books = db.relationship('Library')


class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))
    save_date = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))