from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy as SA
import config 
import mysql.connector

app = Flask('Library Management System')
app.config["SQLALCHEMY_DATABASE_URI"] = config.DEV
db = SA(app)


from models import create_models
create_models(db)


# @app.route('/')
# def index():
#     def db_query():
#         db = Database()
#         emps = db.list_employees()
#         return emps
#     res = db_query()
#     print(res)
#     return render_template('employess.html', result=res, content_type='application/json')