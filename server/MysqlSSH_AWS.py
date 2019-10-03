# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 14:35:05 2019

@author: Jerry
"""

# ssh variables
host = '18.222.199.110'
localhost = '127.0.0.1'
ssh_username = 'ubuntu'
ssh_password = '123456'
#ss_private_key = '/path/to/key.pem'
ss_private_key = 'galera-cluster.pem'
# database variables
user='root'
password='123456'
database='test_db'

from sshtunnel import SSHTunnelForwarder
import MySQLdb as db
import pandas as pd

def query(q):
    with SSHTunnelForwarder(
        (host, 22),
        ssh_username=ssh_username,
        ssh_pkey = ss_private_key,
#        ssh_password = ssh_password,
        #ssh_private_key=private_key,
        remote_bind_address=(localhost, 3306)
    ) as server:
        conn = db.connect(host=localhost,
                               port=server.local_bind_port,
                               user=user,
                               passwd=password,
                               db=database)

        return pd.read_sql_query(q, conn)
    
df = query('select * from test limit 5')