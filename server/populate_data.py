from app import db
import datetime
from flask import g
import sqlalchemy as sa
from sqlalchemy import UniqueConstraint

import config
from models import Book,Subject,Checkout,Inventory

def populate_tables():
    # load_data_from_csv(obj['Book'],'Book')
    # load_data_from_csv(obj['Subject'],'Subject')
    #load_data_from_csv(obj['Checkout'],'Checkout')
    load_data_from_csv(obj['Inventory'],'Inventory')

obj = {
    'Book': {
        'attrKey': [
            {'bibnum': '0'},
            {'title': '2'},
            {'author': '3'},
            {'publisher': '4'}
        ],
        'filePath': '../../ADB Proj Final Data/Book_Table.csv'
    },
    'Subject': {
        'attrKey': [
            {'bibnum': '1'},
            {'subjects': '0'},
        ],
        'filePath': '../../ADB Proj Final Data/Subjects_Table.csv'
    },
    'Checkout': {
        'attrKey': [
            {'checkoutyear': '1'},
            {'bibnum': '2'},
            {'itemtype': '3'},
            {'checkouttime': '4'},
            {'checkoutmonth': '5'},
            {'checkoutday': '6'},
            {'checkoutdate': '7'},
        ],
        'filePath': '../../ADB Proj Final Data/Clean_CheckOutData.csv'
    },
    'Inventory' : {
        'attrKey': [
            {'bibnum': '0'},
            {'entrydate': '1'},
            {'itemcount': '2'}
        ],
        'filePath': '../../ADB Proj Final Data/Inventory_Table.csv'
    }
}
import csv
def load_data_from_csv(dictionary,tablename):
    listObj = []

    with open(dictionary['filePath']) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        i = 0
        print(dictionary)
        for row in csv_reader:
            if line_count != 0:
                obj = {}
                for item in dictionary['attrKey']:
                    for key,value in item.items():
                        obj[key] = row[int(value)].strip()
                listObj.append(obj)
            line_count += 1
        
    print(tablename)
    if tablename == 'Book':
        load_books(listObj)
    elif tablename == 'Subject':
        load_subjects(listObj)
    elif tablename == 'Checkout':
        load_checkout(listObj)
    else:
        load_inventory(listObj)



def load_books(books):
    i = 0
    while i < len(books):
        newBook = None
        newBook = Book(bibnum=books[i]['bibnum'],title=books[i]['title'],authorname=books[i]['author'],publicationname=books[i]['publisher'])
        db.session.add(newBook)
        db.session.commit()
        i += 1
        if i > 20000:
            break

def load_subjects(subjects):
    i = 0
    while i < len(subjects):
        newSubject = None
        existingSubject = db.session.query(Subject).filter(Subject.subjectname == subjects[i]['subjects']).first()
        if existingSubject == None:
            newSubject = Subject(subjectname=subjects[i]['subjects'])
            db.session.add(newSubject)
        else:
            newSubject = existingSubject
        book = db.session.query(Book).filter(Book.bibnum == int(subjects[i]['bibnum'])).first()
        if book is not None:
            newSubject.books.append(book)
        db.session.commit()
        i += 1
        if i > 10000:
            break

def load_checkout(checkoutlist):
    i = 0
    while i < len(checkoutlist):
        newentry = None
        newentry = Checkout(bibnum=int(checkoutlist[i]['bibnum']),itemtype=checkoutlist[i]['itemtype'],checkoutmonth=checkoutlist[i]['checkoutmonth'],checkoutyear=checkoutlist[i]['checkoutyear'],checkoutday=checkoutlist[i]['checkoutday'],checkouttime=checkoutlist[i]['checkouttime'])
        
        book = db.session.query(Book).filter(Book.bibnum == int(checkoutlist[i]['bibnum'])).first()
        if book is not None:
            db.session.add(newentry)
            book.checkoutentry.append(newentry)
        db.session.commit()
        i += 1
        if i > 20000:
            break

def load_inventory(inventory):
    i = 0
    while i < len(inventory):
        newentry = None
        newentry = Inventory(bibnum=int(inventory[i]['bibnum']),itemcount=int(inventory[i]['itemcount']),entrydate=datetime.datetime.strptime(inventory[i]['entrydate'], '%d/%m/%Y'))
        
        book = db.session.query(Book).filter(Book.bibnum == int(inventory[i]['bibnum'])).first()
        if book is not None:
            db.session.add(newentry)
            book.inventoryentry.append(newentry)
        db.session.commit()
        i += 1
        if i > 20000:
            break