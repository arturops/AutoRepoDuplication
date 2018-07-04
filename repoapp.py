
# Web application to automatically duplicate a github repository 
# from one account to another


from flask import Flask, render_template, url_for, flash, redirect, request
from forms import GithubUserForm
import apiwrap
import mistune

app = Flask(__name__)

app.config['SECRET_KEY'] = '2aba1f6ebe92e925ec34c8486003cf08'
app.config['DEBUG'] = True



@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/about')
def about():
	version = {
		'author' : 'Arturo Parrales Salinas',
		'title' : 'Auto Repo Duplication App',
		'ver' : '0.0.0.2',
		'date' : 'July 2, 2018'
	}

	return render_template('about.html', title='About', version=version)


@app.route('/docs')
def docs():
	markdown = mistune.Markdown(escape=True, hard_wrap=True)
	with open('README.md', 'r') as content_file:
			content = content_file.read()
	markup_html = markdown(content)
	return render_template('install.html', title='Installation', markup_html=markup_html)


@app.route('/techinfo')
def techinfo():
	markdown = mistune.Markdown(escape=True, hard_wrap=True)
	with open('TechInfo.md', 'r') as content_file:
			content = content_file.read()
	markup_html = markdown(content)
	return render_template('techinfo.html', title='Info', markup_html=markup_html)


@app.route('/access',methods=['GET','POST'])
def access():
	form = GithubUserForm()
	if form.validate_on_submit():

		# GithubAPI object initialization
		github = apiwrap.GithubAPI(debug=app.config['DEBUG'])
		# redirect to github authorization login
		return redirect(github.get_github_auth_url())

	return render_template('access.html',title='User', form=form)


@app.route('/done')
def done():

	username = ''
	repo = ''
	if request.method == 'GET':

		if 'code' in request.args:

			code = request.args['code']
				
			# GithubAPI object initialization
			github = apiwrap.GithubAPI(debug=app.config['DEBUG'])
			# Get user's token
			github.get_user_token(code) 
			# duplicates repo
			success_repo = github.duplicate_repo()
				

			if success_repo:
				username = github.user.username
				repo = github.user.repo
				success_str = 'Successful Repo Duplication! Thanks!'
				flash(success_str,'success')

				return render_template('thanks.html', title='Thanks', username=username, repo=repo)		

	danger_str = 'Failure duplicating the repo! Sorry!'
	flash(danger_str,'danger')
	return render_template('fail.html', title='Ooops')



# Handles page not found
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

# Handles when API rate limit is exceeded
@app.errorhandler(403)
def rate_limit_exceeded(e):
	return render_template('403.html'),403

# Handles Server Internal errors
@app.errorhandler(500)
def server_error(e):
	return render_template('500.html'),500


# To run in debug mode
if __name__ == '__main__':
	app.run()
