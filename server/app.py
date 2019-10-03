from flask import Flask, render_template,make_response,jsonify
from flask_sqlalchemy import SQLAlchemy as SA
import config 
import mysql.connector
from sqlalchemy import func

from sqlalchemy_serializer import SerializerMixin

app = Flask('Library Management System')
app.config["SQLALCHEMY_DATABASE_URI"] = config.DEV
db = SA(app)


from models import create_models

create_models(db)
from models import Book,Subject,Checkout

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/lms/api/books', methods=['GET'])
def book():
    def getBooks(parameter):
        books = Book.get_books_10()
        return books
    response = getBooks('bookname')
    
    results = []
    for bucketlist in response:
        obj = {
            'name': bucketlist.title
        }
        results.append(obj)
    response = jsonify(results)
    return response