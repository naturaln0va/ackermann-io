from flask import render_template
from app import app

@app.route('/')
@app.route('/home')
def index():
	user = {'name': 'Ryan'}
	return render_template('index.html', title='Home', user=user)