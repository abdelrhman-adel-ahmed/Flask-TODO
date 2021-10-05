from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"Task {self.id}"
