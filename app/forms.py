
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, BooleanField, DateField
from wtforms.validators import DataRequired

from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
	title = StringField('title', validators=[DataRequired()])
	description = StringField('description', validators=[DataRequired()])
	content = PageDownField('content', validators=[DataRequired()])
	category = StringField('category')
	draft = BooleanField('draft', default=True)
	save = SubmitField('save')
	slug = StringField('slug')
	date = DateField('date', default=datetime.utcnow(), format='%b %d, %Y')

class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])