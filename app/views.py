
import os, math, subprocess, json
from random import randint
from functools import wraps
from operator import itemgetter
from flask import request, session, render_template, redirect, url_for, flash, abort, jsonify, Markup
from urllib.parse import urljoin
from werkzeug.utils import secure_filename
from feedwerk.atom import AtomFeed
from datetime import datetime, date
from markdown import markdown as md
from app import app, db
from config import ASSETS_FOLDER
from .forms import PostForm, SearchForm
from .models import Post, Category

# Exception handling

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='Not Found', auth=has_auth()), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title='500', auth=has_auth()), 500

# Helpers

def make_external(url):
	return urljoin(request.url_root, url)

# Authentication

def has_auth():
	return 'username' in session

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if not has_auth():
			return redirect('/login')
		return f(*args, **kwargs)
	return decorated

# Routing

@app.route('/')
def index():
	posts = Post.query.order_by(Post.timestamp.desc()).filter_by(draft=False).all()
	return render_template('index.html', posts=posts, auth=has_auth(), current='index', shape_num=randint(1,9))

@app.route('/deploy', methods=['GET', 'POST'])
def deploy():
	if request.method == 'POST':
		cwd = os.getcwd()
		return jsonify(cwd)
		# subprocess.check_call(['python', 'deployer.py'], cwd='../')
		# return redirect('/')
	else:
		abort(404)

@app.route('/kakao-auth')
def kakao_auth():
	auth_url = 'youversion://kakao-auth'

	if len(request.query_string) > 0:
		auth_url += '?' + request.query_string

	return redirect(auth_url)
	
@app.route('/hackz')
def hacks():
	return redirect('https://ackermann.io/static/assets/deploy.zip')

@app.route('/posts/<slug>')
def post_view(slug):
	post = Post.query.filter_by(slug=slug).first()

	word_count = len(post.content.split())
	dur = int(math.ceil(word_count / 200))

	if dur < 3:
		dur = None
		
	today = date.today()
	cpwy = today.year

	return render_template('view_post.html', title=post.title, post=post, dur=dur, cpwy=cpwy, auth=has_auth(), current='home')

@app.route('/categories')
def categories():
	dicts = []
	for c in Category.query.order_by(Category.name).all():
		none_draft_posts = c.posts.filter_by(draft=False).all()
		if len(none_draft_posts) > 0:
			dicts.append({'name': c.name, 'posts': none_draft_posts})
	return render_template('categories.html', dicts=dicts, auth=has_auth(), current='categories')

@app.route('/search/results/<query>')
def search_results(query):
	posts = Post.query.filter(Post.title.ilike('%'+query+'%')).order_by(Post.timestamp.desc()).filter_by(draft=False).all()
	return render_template('search.html', query=query, posts=posts, auth=has_auth())

@app.route('/apps')
@app.route('/portfolio')
def portfolio():
	return render_template('portfolio.html', auth=has_auth(), current='portfolio')

@app.route('/links')
@app.route('/about')
def about():
	today = date.today()
	my_age = today.year - 1994 - ((today.month, today.day) < (11, 26))
	return render_template('about.html', auth=has_auth(), current='about', age=my_age)

@app.route('/privacy')
def privacy():
	return render_template('privacy.html', title='Privacy', auth=has_auth())

@app.route('/quakes')
def quakes():
	return render_template('quakes.html', title='Quakes', auth=has_auth())

@app.route('/feed')
def feed():
	icon_url = make_external('/static/favicon/apple-touch-icon.png')
	feed = AtomFeed('Ryan Ackermann', subtitle='My recent posts', logo=icon_url, feed_url=request.url, url=request.url_root)
	posts = Post.query.order_by(Post.timestamp.desc()).filter_by(draft=False).limit(10).all()
	author_name = 'Ryan Ackermann'
	for post in posts:
		url = make_external(post.url())
		content = Markup(md(post.content))
		feed.add(post.title, content, content_type='html', author=author_name, url=url, updated=post.timestamp, published=post.timestamp)
	return feed.get_response()
	
@app.route('/resume')
def resume():
	return redirect('https://ackermann.io/static/assets/resume.pdf')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if has_auth():
		return redirect('/')
	
	if request.method == 'POST':		
		try:
			with open('pw.txt', 'r') as file:
				password = file.read().replace('\n', '')
				
				if request.form['password'] == password:
					session['username'] = 'naturaln0va'
					return redirect('/')
		except BaseException as err:
			print('An exception occurred {}'.format(err))
			return redirect('/')
	return render_template('login.html', auth=has_auth())

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect('/')

@app.route('/drafts')
@requires_auth
def drafts():
	drafts = Post.query.order_by(Post.timestamp.desc()).filter_by(draft=True).all()
	return render_template('drafts.html', drafts=drafts, auth=has_auth(), current='drafts')

@app.route('/drafts/<slug>')
def draft_view(slug):
	draft = Post.query.filter_by(draft=True).filter_by(slug=slug).first()
	return render_template('view_post.html', title=draft.title, post=draft, auth=has_auth())

@app.route('/drafts/edit/<int:draft_id>', methods = ['GET', 'POST'])
@requires_auth
def draft_edit(draft_id):
	draft = Post.query.get(draft_id)
	form = PostForm()
	if request.method == 'GET':
		form.title.data = draft.title
		form.description.data = draft.description
		form.content.data = draft.content
		form.draft.data = draft.draft
		form.category.data = draft.category.name
		form.date.data = draft.timestamp
		form.slug.data = draft.slug
	if form.validate_on_submit():
		draft.title = form.title.data
		draft.description = form.description.data
		draft.content = form.content.data
		draft.draft = form.draft.data
		draft.timestamp = form.date.data
		draft.slug = form.slug.data
		# if there is an exsisting category use it
		category = Category.query.filter_by(name=form.category.data).first()
		if not category:
			category = Category(form.category.data)
		draft.category = category
		db.session.commit()
		return redirect('/drafts')
	return render_template('new_post.html', form=form, auth=has_auth())

@app.route('/drafts/rm/<int:draft_id>')
@requires_auth
def delete_draft(draft_id):
	draft = Post.query.get(draft_id)
	db.session.delete(draft)
	db.session.commit()
	return redirect('/drafts')

@app.route('/drafts/publish/<int:draft_id>')
@requires_auth
def publish_draft(draft_id):
	post = Post.query.get(draft_id)
	post.draft = False
	post.timestamp = datetime.utcnow()
	db.session.commit()
	return redirect('/')

@app.route('/posts/create', methods = ['GET', 'POST'])
@requires_auth
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		title = form.title.data
		description = form.description.data
		content = form.content.data
		draft = form.draft.data
		date = form.date.data
		# if there is an exsisting category use it
		category = Category.query.filter_by(name=form.category.data).first()
		if not category:
			category = Category(form.category.data)
		post = Post(title, description, content, category)
		post.draft = draft
		post.timestamp = date
		db.session.add(post)
		db.session.commit()
		return redirect('/drafts')
	else:
		print('Errors in the form:')
		print(form.errors.items())
	return render_template('new_post.html', form=form, auth=has_auth(), current='new_post')

@app.route('/cms', methods=['GET', 'POST'])
@requires_auth
def cms():
	if request.method == 'POST':
		for file in request.files.getlist("file[]"):
			filename = secure_filename(file.filename)
			file.save(os.path.join(ASSETS_FOLDER, filename))
		return redirect('/cms')
	else:
		if not os.path.exists(ASSETS_FOLDER):
			os.makedirs(ASSETS_FOLDER)
		dicts = []
		for filename in os.listdir(ASSETS_FOLDER):
			dicts.append({'name': filename, 'size': os.path.getsize(os.path.join(ASSETS_FOLDER, filename))})
		sorted_items = sorted(dicts, key=itemgetter('name'))
		return render_template('cms.html', items=sorted_items, auth=has_auth(), current='cms')

@app.route('/cms/rm/<filename>')
@requires_auth
def delete_file(filename):
	os.remove(os.path.join(ASSETS_FOLDER, filename))
	return redirect('/cms')
