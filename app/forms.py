
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired

from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
	title = StringField('title', validators=[DataRequired()])
	description = StringField('description', validators=[DataRequired()])
	content = PageDownField('post contents', validators=[DataRequired()])
	draft = BooleanField('Draft', default=True)
	save = SubmitField('Save')