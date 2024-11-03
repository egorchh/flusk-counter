import time
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Counter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

def log_request():
    client_info = request.headers.get('User-Agent')
    new_counter = Counter(client_info=client_info)
    db.session.add(new_counter)
    db.session.commit()

@app.route('/')
def hello():
    log_request()
    count = Counter.query.count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
