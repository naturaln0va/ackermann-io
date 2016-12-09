
import os
from operator import itemgetter
from flask import request, session, render_template, redirect, url_for, flash
from flask_mail import Message
from werkzeug.utils import secure_filename
from datetime import datetime
from app import app, db, mail
from config import UPLOAD_FOLDER
from .forms import PostForm, SearchForm
from .models import Post, Category

# Exception handling

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='404', auth=has_auth()), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title='500', auth=has_auth()), 500

# Authentication

def has_auth():
	return 'username' in session

# Routing

@app.route('/')
def index():
	posts = Post.query.order_by(Post.timestamp.desc()).filter_by(draft=False).all()
	return render_template('index.html', posts=posts, auth=has_auth())

@app.route('/categories')
def categories():
	dicts = []
	for c in Category.query.order_by(Category.name).all():
		if len(c.posts.filter_by(draft=False).all()) > 0:
			dicts.append({'name': c.name, 'posts': c.posts})
	return render_template('categories.html', dicts=dicts, auth=has_auth())

@app.route('/posts/<slug>')
def post_view(slug):
	post = Post.query.filter_by(slug=slug).first()
	return render_template('view_post.html', title=post.title, post=post, auth=has_auth())

@app.route('/login', methods=['GET', 'POST'])
def login():
	if has_auth():
		return redirect('/')
	if request.method == 'POST' and request.form['password'] == 'EQjmLRVwDX%;z&Ek94N(Fa7C6MGinbgmpg':
		session['username'] = 'naturaln0va'
		return redirect('/')
	return render_template('login.html', auth=has_auth())

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect('/')

@app.route('/apps')
@app.route('/about')
@app.route('/portfolio')
def portfolio():
	return render_template('portfolio.html', auth=has_auth())

@app.route('/privacy')
def privacy():
	return render_template('privacy.html', title='Privacy', auth=has_auth())

@app.route('/quakes')
def quakes():
	return render_template('quakes.html', title='Quakes', auth=has_auth())

@app.route('/drafts')
def drafts():
	if not has_auth():
		return redirect('/login')
	drafts = Post.query.order_by(Post.timestamp.desc()).filter_by(draft=True).all()
	return render_template('drafts.html', drafts=drafts, auth=has_auth())

@app.route('/drafts/<slug>')
def draft_view(slug):
	draft = Post.query.filter_by(draft=True).filter_by(slug=slug).first()
	return render_template('view_post.html', title=draft.title, post=draft, auth=has_auth())

@app.route('/drafts/edit/<int:draft_id>', methods = ['GET', 'POST'])
def draft_edit(draft_id):
	if not has_auth():
		return redirect('/login')
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
		db.session.commit()
		return redirect('/drafts')
	return render_template('new_post.html', form=form, auth=has_auth())

@app.route('/drafts/rm/<int:draft_id>')
def delete_draft(draft_id):
	if not has_auth():
		return redirect('/login')
	draft = Post.query.get(draft_id)
	db.session.delete(draft)
	db.session.commit()
	return redirect('/drafts')

@app.route('/drafts/publish/<int:draft_id>')
def publish_draft(draft_id):
	if not has_auth():
		return redirect('/login')
	post = Post.query.get(draft_id)
	post.draft = False
	post.timestamp = datetime.utcnow()
	db.session.commit()
	return redirect('/')

@app.route('/posts/create', methods = ['GET', 'POST'])
def new_post():
	if not has_auth():
		return redirect('/login')
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
		print 'Errors in the form:'
		print form.errors.items()
	return render_template('new_post.html', form=form, auth=has_auth())

@app.route('/cms', methods=['GET', 'POST'])
def cms():
	if not has_auth():
		return redirect('/login')
	if request.method == 'POST':
		for file in request.files.getlist("file[]"):
			filename = secure_filename(file.filename)
			file.save(os.path.join(UPLOAD_FOLDER, filename))
		return redirect('/cms')
	else:
		if not os.path.exists(UPLOAD_FOLDER):
			os.makedirs(UPLOAD_FOLDER)
		dicts = []
		for filename in os.listdir(UPLOAD_FOLDER):
			dicts.append({'name': filename, 'size': os.path.getsize(os.path.join(UPLOAD_FOLDER, filename))})
		sorted_items = sorted(dicts, key=itemgetter('name'))
		return render_template('cms.html', items=sorted_items, auth=has_auth())

@app.route('/cms/rm/<filename>')
def delete_file(filename):
	if not has_auth():
		return redirect('/login')
	os.remove(os.path.join(UPLOAD_FOLDER, filename))
	return redirect('/cms')

@app.route('/search/results/<query>')
def search_results(query):
	posts = Post.query.filter(Post.title.ilike('%'+query+'%')).all()
	return render_template('search.html', query=query, posts=posts, auth=has_auth())
