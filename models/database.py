from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class galleryPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), unique=True, nullable=False)
    
    def __init__(self, filename):
        self.filename = filename