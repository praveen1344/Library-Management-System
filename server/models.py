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
    
    def make_dict(self):
        inventoryEntry = list(entry.make_dict() for entry in self.inventoryentry)
        checkoutEntry = list(entry.make_dict() for entry in self.checkoutentry)
        
        return {'bibnum': self.bibnum, 'title': self.title, 'author': self.authorname, 'publication': self.publicationname, 'inventory': inventoryEntry,'checkout': checkoutEntry}

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

    def make_dict(self):
        # return {'checkoutid': self.checkoutid, 'bibnum': self.bibnum, 'itemtype': self.itemtype, 'checkoutmonth': self.checkoutmonth, 'checkoutyear': self.checkoutyear, 'checkoutday': self.checkoutday, 'checkouttime': self.checkouttime }
        return {'id': self.checkoutid, 'itemtype': self.itemtype, 'checkoutmonth': self.checkoutmonth, 'checkoutyear': self.checkoutyear, 'checkoutday': self.checkoutday, 'checkouttime': self.checkouttime }

class Inventory(db.Model):
    __tablename__ = 'Inventory'

    inventoryid = db.Column(db.Integer, nullable=False, primary_key=True, auto_increment=True)
    bibnum      = db.Column(db.Integer, db.ForeignKey('Book.bibnum'))
    entrydate   = db.Column(db.DateTime)
    itemcount   = db.Column(db.Integer)

    def make_dict(self):
        # return {'entry': self.inventoryid, 'bibnum': self.bibnum, 'entrydate': str(self.entrydate), 'itemcount': self.itemcount}
        return {'id': self.inventoryid, 'entrydate': str(self.entrydate), 'itemcount': self.itemcount}


from populate_data import populate_tables


def create_models(db):
    db.create_all()
    
    if db.session.query(Book).first() is None:
        populate_tables()