from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CodeBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(500))
