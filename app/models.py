
from app import db
from datetime import datetime
from slugify import slugify

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    content = db.Column(db.String)
    slug = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    draft = db.Column(db.Boolean, default=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, description, content, category=None):
        self.title = title
        self.description = description
        self.content = content
        self.timestamp = datetime.utcnow()
        self.slug = slugify(title)
        self.category = category

    def __repr__(self):
        return '<Post [%r] %r - %r>' % self.slug % self.title % self.category

    def url(self):
        return '/posts/' + self.slug

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name