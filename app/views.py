
import os
from flask import request, session, render_template, redirect, flash
from werkzeug.utils import secure_filename
from app import app, db
from config import UPLOAD_FOLDER
from .forms import PostForm
from .models import Post

# Exception handling

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='404'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title='500'), 500

# Authentication

def has_auth():
	return 'username' in session

# Routing

@app.route('/')
def index():
	posts = Post.query.filter_by(draft=False).all()
	return render_template('index.html', posts=posts, auth=has_auth())

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
	drafts = Post.query.filter_by(draft=True)
	return render_template('drafts.html', drafts=drafts, auth=has_auth())

@app.route('/drafts/<slug>')
def draft_view(slug):
	draft = Post.query.filter_by(slug=slug).first()
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
	if form.validate_on_submit():
		draft.title = form.title.data
		draft.description = form.description.data
		draft.content = form.content.data
		draft.draft = form.draft.data
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
	db.session.commit()
	return redirect('/')

@app.route('/new_post', methods = ['GET', 'POST'])
def new_post():
	if not has_auth():
		return redirect('/login')
	form = PostForm()
	if form.validate_on_submit():
		title = form.title.data
		description = form.description.data
		content = form.content.data
		draft = form.draft.data

		print '\n***\nTitle: ' + title + '\nDescription: ' + description + '\nData: ' + content + '\nDraft: ' + str(draft) + '\n***\n'

		post = Post(title, description, content)
		db.session.add(post)
		db.session.commit()

		return redirect('/drafts')
	return render_template('new_post.html', form=form, auth=has_auth())

@app.route('/cms', methods=['GET', 'POST'])
def cms():
	if not has_auth():
		return redirect('/login')
	if request.method == 'POST':
		file = request.files['file']
		filename = secure_filename(file.filename)
		file.save(os.path.join(UPLOAD_FOLDER, filename))
		return redirect('/cms')
	else:
		dicts = []
		for filename in os.listdir(UPLOAD_FOLDER):
			dicts.append({'name': filename, 'size': os.path.getsize(os.path.join(UPLOAD_FOLDER, filename))})
		return render_template('cms.html', items=dicts, auth=has_auth())

@app.route('/cms/rm/<filename>')
def delete_file(filename):
	if not has_auth():
		return redirect('/login')
	os.remove(os.path.join(UPLOAD_FOLDER, filename))
	return redirect('/cms')
