from app import db
import datetime
from flask import g
import sqlalchemy as sa
from sqlalchemy import UniqueConstraint

import config

subject_mapping = db.Table('SubjectBook', 
    db.Column('bookid', db.Integer, db.ForeignKey('Book.bibnum', primary_key=True)),
    db.Column('subjectid', db.Integer, db.ForeignKey('Subject.subjectid'), primary_key=True)
)

author_mapping = db.Table('AuthorBook', 
    db.Column('bookid', db.Integer, db.ForeignKey('Book.bibnum', primary_key=True)),
    db.Column('authorid', db.Integer, db.ForeignKey('Author.authorid'), primary_key=True)
)

publication_mapping = db.Table('PublicationBook', 
    db.Column('bookid', db.Integer, db.ForeignKey('Book.bibnum', primary_key=True)),
    db.Column('publicationid', db.Integer, db.ForeignKey('Publication.publicationid'), primary_key=True)
)

class Subject(db.Model):
    __tablename__ = 'Subject'

    subjectid = db.Column(db.Integer, nullable = False, primary_key = True, autoincrement = True)
    subjectname = db.Column(db.Text, nullable = False)
    books = db.relationship('Book',secondary=subject_mapping, backref=db.backref("subjects"),lazy="select")

class Book(db.Model):
    __tablename__ = 'Book'

    bibnum = db.Column(db.Integer, nullable=False, primary_key = True)
    booktitle = db.Column(db.Text)
    # inventoryitems = relationship("Inventory")

class Author(db.Model):
    __tablename__ = 'Author'

    authorid = db.Column(db.Integer,nullable=False,primary_key=True)
    authorname = db.Column(db.Text,nullable=False)
    books = db.relationship('Book',secondary=author_mapping,backref=db.backref("authors"),lazy="select")

class Publication(db.Model):
    __tablename__ = 'Publication'

    publicationid = db.Column(db.Integer,nullable=False,primary_key=True)
    publishername = db.Column(db.Text, nullable=False)
    books = db.relationship('Book',secondary=publication_mapping,backref=db.backref("publication"),lazy="select")

# class Inventory(db.Model):
#     __tablename__ = 'Inventory'

#     inventoryid =  db.Column(db.Integer,nullable=False,primary_key=true)
#     reportdate  =  db.Column(db.DateTime,nullable=False)
#     itemcount   =  db.Column(db.Integer,nullable=False)
#     bookid = db.Column(db.Integer, db.ForeignKey('Book.bibnum'))

def create_models(db):
    db.create_all()
    load_books()
    load_subjects()
    load_authors()
    load_publishers()


import csv

def load_subjects():
    subjects = []
    each_subject = {}
    with open('data/Subject_Short.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                each_subject = {}
                each_subject['Subjects'] = row[0]
                each_subject['bibnum'] = row[1]
                line_count += 1
                subjects.append(each_subject)

    print(len(subjects),subjects[0]['bibnum'])
    i = 0
    while i < len(subjects):
        newSubject = None
        newSubject = Subject(subjectname=subjects[i]['Subjects'])
        db.session.add(newSubject)
        # print(int(subjects[i]['bibnum']))
        # book = db.session.query(Book.bibnum == int(subjects[i]['bibnum']))
        book = db.session.query(Book).filter(Book.bibnum == int(subjects[i]['bibnum'])).first()
        # print(book.first())
        if book is not None:
            newSubject.books.append(book)
        db.session.commit()
        i += 1

    print('Done')

def load_authors():

    authors = []

    with open('data/Author_Short.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                authorObject = {}
                authorObject['bibnum'] = row[0]
                authorObject['authorname'] = row[1]
                line_count += 1
                authors.append(authorObject)

    i = 0
    while i < len(authors):
        newAuthor = None
        newAuthor = Author(authorname=authors[i]['authorname'])
        db.session.add(newAuthor)
        associatedbook = db.session.query(Book).filter(Book.bibnum == int(authors[i]['bibnum'])).first()
        if associatedbook is not None:
            newAuthor.books.append(associatedbook)
        db.session.commit()
        i += 1

def load_publishers():
    publishers = []

    with open('data/Publisher.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                publisherObject = {}
                publisherObject['bibnum'] = row[0]
                publisherObject['publishername'] = row[1]
                line_count += 1
                publishers.append(publisherObject)

    i = 0
    while i < len(publishers):
        newPublisher = None
        newPublisher = Publication(publishername=publishers[i]['publishername'])
        db.session.add(newPublisher)
        associatedbook = db.session.query(Book).filter(Book.bibnum == int(publishers[i]['bibnum'])).first()
        if associatedbook is not None:
            newPublisher.books.append(associatedbook)
        db.session.commit()
        i += 1

def load_books():

    books = []

    with open('data/Book_Short.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                each_book = {}
                each_book['bibnum'] = row[0]
                each_book['title'] = row[1]
                line_count += 1
                books.append(each_book)

    print(len(books),books[0]['bibnum'])
    i = 0
    while i < len(books):
        newBook = None
        newBook = Book(bibnum=books[i]['bibnum'],booktitle=books[i]['title'])
        db.session.add(newBook)
        db.session.commit()
        i += 1

    print('Done')