from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    client_info = db.Column(db.String(256))

    def __repr__(self):
        return f'<Counter {self.id} at {self.datetime}>'
