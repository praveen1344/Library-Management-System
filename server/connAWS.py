# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 13:05:16 2019

@author: Jerry
"""
from flask import Flask
from sshtunnel import SSHTunnelForwarder
from flask_sqlalchemy import SQLAlchemy

def dbConn():
    # ssh variables
    host = '18.222.199.110'
    localhost = '127.0.0.1'
    ssh_username = 'ubuntu'
#    ssh_password = '123456'
    ss_public_key = 'galera-cluster.pem'
    # database variables
    user='root'
    password='123456'
    database='LibraryInventory'
    app = Flask(__name__)
    server =  SSHTunnelForwarder(
         (host, 22),
#         ssh_password= ssh_password,
         ssh_pkey = ss_public_key,
         ssh_username = ssh_username,
         remote_bind_address=(localhost, 3306))
    
    server.start()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:{}/LibraryInventory'.format(server.local_bind_port)
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://127.0.0.1'
    db = SQLAlchemy(app)
    return db
    
#server.stop()