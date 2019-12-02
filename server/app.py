from flask import Flask, jsonify
from flask_pymongo import PyMongo
import json
from pymongo import MongoClient
from flask_restful import Resource,Api,reqparse
import re
from flask_cors import CORS
import operator
import pandas as pd
from ItemTypeHashmap import mapping as ItemTypeMapping

app = Flask('Seattle Library Management')
cors = CORS(app)
app.config['MONGO_DB'] = 'seattle-library'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/' + app.config['MONGO_DB']
print(app.config['MONGO_URI'])
mongo = PyMongo(app)

client = MongoClient()
db = client['seattle-library']
collection = db.books

parser = reqparse.RequestParser()
#Load data into the MongoDB Datastore
@app.route('/lms/api/dataload', methods=['GET'])
def data_load():
    # with open('../../ADB Proj Final Data/JSON/FinalAggregate_1000.json') as json_file:
    with open('../../ADB Proj Final Data/JSON/FinalAggregrate.json') as json_file:
        objects = json.load(json_file)
        i = 0
        for row in objects:
            row['inventory'] = row['inventory'][0]
            row['inventory']['entrydate'] = "2019-01-09 00:00:00"

        print(len(objects))
    collection.insert_many(objects)
    return {'response':'200'}

#Get books based on title. Get suggested books based on the subject of input book title
@app.route('/lms/api/book', methods=['GET'])
def getBookByTitle():
    parser.add_argument('title', type=str)
    args = parser.parse_args()
    
    title = '.*' + args['title'].strip() + '.*'
    
    response = collection.find({'title': re.compile(title + '$', re.IGNORECASE), 'inventory.itemcount': { '$gte': 1 }}).limit(1)
    output = []
    similairBooks = []
    subjectlist = []
    bibnum = None
    for s in response:
        bibnum = s['bibnum']
        checkout = s['checkout']
        checkoutcount = inventorycount = 0
        inventorycount = s['inventory']['itemcount']
        for elem in checkout:
            if elem['checkoutmonth'] == 9 and elem['checkoutyear'] == 2019:
                checkoutcount += 1
        
        availablecount = inventorycount - checkoutcount

        if availablecount < 0:
                availablecount = 0

        output.append({'bibnum' : s['bibnum'], 'title' : s['title'], 'authorname': s['author'],'publicationname': s['publication'], 'count': availablecount})
        if 'subjectslist' in s:
            subjectlist = s['subjectslist']


    if len(subjectlist) > 0:
        similairBooksQuery = collection.find({'subjectslist': { '$in' : subjectlist}}).limit(100)
        for s in similairBooksQuery:
            if s['bibnum'] != bibnum:
                similairBooks.append({'bibnum' : s['bibnum'], 'title' : s['title'], 'authorname': s['author'], 'publicationname': s['publication'], 'count': s['inventory']})
            
    return jsonify({'book': output, 'suggestions': similairBooks})

# Trial API just to get the list of Authors who have more than one book published and present in the Seattle Library
@app.route('/lms/api/authorcheck', methods=['GET'])
def checkmultipleauthor():
    parser.add_argument('title', type=str)
    args = parser.parse_args()
    
    response = collection.find()
    output = {}
    for s in response:
        if s['author'] in output:
            output[s['author']]['count'] += 1
        else:
            objectA = {
                'count' : 1
            }
            output[s['author']] = objectA
    
    for elem in output:
        if output[elem]['count'] > 10:
            print('Found', output[elem])
    return {'response':'200'}

#For a given author, the most popular format for their publications will be displayed 
#which could contribute as a suggestion for their future publications
@app.route('/lms/api/compareCheckoutsByPublishedType', methods=['GET'])
def getCheckoutByItemType():
    parser.add_argument('authorname', type=str)
    args = parser.parse_args()
    authorNameInput = args['authorname']
    
    author = args['authorname'].strip()
    
    response = collection.find({'author': author})

    itemTypeHash = {}
    output = []
    for s in response:
        if len(s['checkout']) > 0:
            for elem in s['checkout']:
                if elem['itemtype'] in itemTypeHash:
                    itemTypeHash[elem['itemtype']] += 1
                else:
                    itemTypeHash[elem['itemtype']] = 1
    
    for elem in list(itemTypeHash.keys()):
        output.append({
            'AuthorName': authorNameInput,
            'itemtype': elem,
            'count': itemTypeHash[elem]
        })
        
    return {'response': output}

#Find Books that need to be purchased for the library
@app.route('/lms/api/purchaseBooks', methods=['GET'])
def getBooksToBePurchased():
    purchase = []
    lt_count = int()
    output = []
    result = collection.find({'checkout.checkoutyear':2019,'checkout.itemtype': {'$in': ItemTypeMapping}})
    i = 0
    for book in result:
        item = {}
        lt_count = 0
        i+=1
        item['title'] = book['title']
        item['bibnum'] = book['bibnum']
        for checkout in book['checkout']:
            lt_count += 1
        item['Count'] = lt_count
        
        purchase.append(item)
    purchase.sort(key=lambda x: x['Count'], reverse=True)
    output = purchase[0:30]
    
    return {'response': output}

#Find Books that can be retired from the library
@app.route('/lms/api/retireBooks', methods=['GET'])
def retireBooks():
    output = []
    
    result = collection.find({'inventory.itemcount':{'$gte': 50},'checkout': {'$size': 0}}).sort('inventory.itemcount',-1).limit(30)
    
    i = 0
    for book in result:
        output.append({'bibnum': book['bibnum'], 'title': book['title'], 'itemcount': book['inventory']['itemcount']})
    # print(output)
    return {'response': output}