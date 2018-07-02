

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class GithubUserForm(FlaskForm):
	#github_username = StringField('Username', validators=[DataRequired(),Length(min=2, max=30)])

	#target_repo = StringField('Target Repo Name', validators=[DataRequired()])


	submit = SubmitField('Get Code!')
