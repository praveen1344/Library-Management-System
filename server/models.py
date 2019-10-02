from app import db
import datetime
from flask import g
import sqlalchemy as sa
from sqlalchemy import UniqueConstraint


import config



class Subjects(db.Model):
    __tablename__ = 'Subjects'

    SubjectID   = db.Column(db.Integer, nullable = False, primary_key = True, autoincrement = True)
    SubjectName = db.Column(db.String(100), nullable = False)
    BibNum      = db.Column(db.String(20), nullable = False)

def create_models(db):

    db.create_all()
    