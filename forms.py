

from flask_wtf import FlaskForm
from wtforms import SubmitField


class GithubUserForm(FlaskForm):

	submit = SubmitField('Get Code!')
