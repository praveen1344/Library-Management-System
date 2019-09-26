from flask import Flask

app = Flask('Library Management System')

@app.route('/')
def index():
    return 'Hello World'