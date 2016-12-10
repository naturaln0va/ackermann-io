
# How to run on Heroku:
# $ heroku run --app flask-ackermann-io create

from app import db

db.drop_all()
db.create_all()
