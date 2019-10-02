import connAWS

db = connAWS.dbConn()

class Subject(db.Model):
    __tablename__ = 'Subject'

    subjectid = db.Column('subjectid', db.Integer, primary_key=True)
    subjectname = db.Column('subjectname', db.String)
    
    def __init__(self, subjectid, subjectname):
        self.subjectid = subjectid
        self.subjectname = subjectname

class Book(db.Model):
    __tablename__ = 'Book'
    bibnum = db.Column('bibnum', db.String, primary_key=True)
    title = db.Column('title', db.String)
    author_name = db.Column('publication_name', db.String)
    
    def __init__(self, bibnum, title, author_name):
        self.bibnum = bibnum
        self.title = title
        self.author_name = author_name
        
class SubjectBook(db.Model):
    __tablename__ = 'SubjectBook'
    subbookid = db.Column('subbookid', db.Integer, primary_key=True)
    subjectid = db.Column('subjectid', db.Integer)
    bibnum = db.Column('bibnum', db.String)
    
    def __init__(self, subbookid, subjectid, bibnum):
        self.subbookid = subbookid
        self.subjectid = subjectid
        self.bibnum = bibnum

class Checkout(db.Model):
    __tablename__ = 'Checkout'
    checkoutid = db.Column('checkoutid', db.Float, primary_key=True)
    bibnum = db.Column('bibnum', db.String)
    checkoutmonth = db.Column('checkoutmonth', db.String)
    itemtype = db.Column('itemtype', db.String)
    checkoutyear = db.Column('checkoutyear', db.String)
    checkouttime = db.Column('checkouttime', db.String)
    
    def __init__(self,checkoutid,bibnum,checkoutmonth,itemtype,checkoutyear,checkouttime):
        self.checkoutid = checkoutid
        self.bibnum = bibnum
        self.checkoutmonth = checkoutmonth
        self.itemtype = itemtype
        self.checkoutyear = checkoutyear
        self.checkouttime = checkouttime

db.create_all()
import pandas as pd
df = pd.read_csv("E:\Commn\MS\ISTM622\Clean_CheckOutData.csv")
#checkout = df.values.tolist()
for index, item in df.iterrows():
    db.session.merge(Checkout(item['ID'],item['BibNumber'],item['CheckOutMonth'],item['ItemType'],item['CheckoutYear'],item['CheckOutTime']))
    if index == 100:break
db.session.commit()