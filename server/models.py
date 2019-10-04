from app import db
import datetime
from flask import g
import sqlalchemy as sa
from sqlalchemy import UniqueConstraint

import config

from sqlalchemy.inspection import inspect

subject_mapping = db.Table('SubjectBook', 
    db.Column('bibnum', db.Integer, db.ForeignKey('Book.bibnum', primary_key=True)),
    db.Column('subjectid', db.Integer, db.ForeignKey('Subject.subjectid'))
)

class Book(db.Model):
    __tablename__ = 'Book'

    bibnum          = db.Column(db.Integer, nullable=False, primary_key=True)
    title           = db.Column(db.Text, nullable = False)
    authorname      = db.Column(db.Text)
    publicationname = db.Column(db.Text)
    inventoryentry  = db.relationship('Inventory', backref="book")
    checkoutentry   = db.relationship('Checkout', backref="Checkout")

    @staticmethod
    def get_books_10():
        return Book.query.limit(10).all()

class Subject(db.Model):
    __tablename__ = 'Subject'

    subjectid   = db.Column(db.Integer, nullable=False, primary_key=True, auto_increment=True)
    subjectname = db.Column(db.Text, nullable = False)
    books = db.relationship('Book',secondary=subject_mapping, backref=db.backref("subjects"), lazy="select")

class Checkout(db.Model):
    __tablename__ = 'Checkout'

    checkoutid    = db.Column(db.Integer, nullable=False, primary_key=True, auto_increment=True)
    bibnum        = db.Column(db.Integer, db.ForeignKey('Book.bibnum'))
    itemtype      = db.Column(db.Text)
    checkoutmonth = db.Column(db.Integer)
    checkoutyear  = db.Column(db.Integer)
    checkoutday  = db.Column(db.Integer)
    checkouttime  = db.Column(db.Text)

class Inventory(db.Model):
    __tablename__ = 'Inventory'

    inventoryid = db.Column(db.Integer, nullable=False, primary_key=True, auto_increment=True)
    bibnum      = db.Column(db.Integer, db.ForeignKey('Book.bibnum'))
    entrydate   = db.Column(db.DateTime)
    itemcount   = db.Column(db.Integer)


from populate_data import populate_tables


def create_models(db):
    db.create_all()
    # print('bbb', db.session.query(Book).first())
    # print('aaa ',db.session.execute('SELECT True FROM Book LIMIT 1'))
    
    if db.session.query(Book).first() is None:
        populate_tables()