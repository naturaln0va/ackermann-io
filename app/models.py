
from app import db
from datetime import datetime
from slugify import slugify

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(1024))
    content = db.Column(db.String(1024 * 1024 * 4))
    slug = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)
    draft = db.Column(db.Boolean, default=True)

    def __init__(self, title, description, content):
        self.title = title
        self.description = description
        self.content = content
        self.timestamp = datetime.utcnow()
        self.slug = slugify(title)

    def __repr__(self):
        return '<Post [%r] %r - %r>' % self.slug % self.title % self.content