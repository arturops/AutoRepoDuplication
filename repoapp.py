
# Web application to automatically duplicate a github repository 
# from one account to another


from flask import Flask, render_template, url_for, flash, redirect, request
from forms import GithubUserForm
import apiwrap
import mistune

# Start the app
app = Flask(__name__)

# App configuration
app.config['SECRET_KEY'] = '2aba1f6ebe92e925ec34c8486003cf08'
app.config['DEBUG'] = False


# Home page
@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')


# About page
@app.route('/about')
def about():
	version = {
		'author' : 'Arturo Parrales Salinas',
		'title' : 'Auto Repo Duplication App',
		'ver' : '0.0.0.2',
		'date' : 'July 2, 2018'
	}

	return render_template('about.html', title='About', version=version)


# Documentation - Installation manual
@app.route('/docs')
def docs():
	markdown = mistune.Markdown(escape=True, hard_wrap=True)
	with open('README.md', 'r') as content_file:
			content = content_file.read()
	markup_html = markdown(content)
	return render_template('install.html', title='Installation', markup_html=markup_html)


# Documentation - Technical description of the repo duplication process flow 
@app.route('/techinfo')
def techinfo():
	markdown = mistune.Markdown(escape=True, hard_wrap=True)
	with open('TechInfo.md', 'r') as content_file:
			content = content_file.read()
	markup_html = markdown(content)
	return render_template('techinfo.html', title='Info', markup_html=markup_html)


# Route with form for the user to click a button and get the app code in his/her Github
# After the click , it redirects to Github to start the authorization process of the app
# to access the user's Github via the Github API (OAuth) 
@app.route('/access',methods=['GET','POST'])
def access():
	form = GithubUserForm()
	if form.validate_on_submit():

		# GithubAPI object initialization
		github = apiwrap.GithubAPI(debug=app.config['DEBUG'])
		# redirect to github authorization login
		return redirect(github.get_github_auth_url())

	return render_template('access.html',title='User', form=form)


# Route where Github redirects after authorization
# Here happens the user's token retrieval and the repo duplication all via Github API
# There is a check to display if the repository was duplicated properly. Cases are:
#
#	1. No "code" received from Github, displays message:
#			'Ooops Github did not send a code to start the process or
#				you got here the wrong way! Sorry! Please click Try Again!'
#
#	2. "Code" received is invalid to exchange for a Github's user token or the token
#		retrieval failed, displays message:
#			'Code from Github is not valid or no access token obtained to start the process!
#								 Sorry! Please click Try Again!'
#	
#	3. "Code" received was valid and token obtained, but failed to duplicate repo,
#		displays message:
#					'Failure duplicating the repo! Sorry! Please Try Again!'
#
#	4. No GET request received, displays message:
#			'This page only processes GET requests with a valid code from Github for an OAuth app!'
#
# 	5. Success duplicating the repo, displays message:
#							'Successful Repo Duplication! Thanks!'
#
@app.route('/done')
def done():

	username = ''
	repo = ''
	danger_str = ''
	if request.method == 'GET':

		if 'code' in request.args:

			code = request.args['code']
				
			# GithubAPI object initialization
			github = apiwrap.GithubAPI(debug=app.config['DEBUG'])
			
			# Get user's token
			success_token = github.get_user_token(code) 
			# check if the token was retrieved properly otherwise code might be invalid
			if success_token is False: 
				danger_str = 'Code from Github is not valid or no access token obtained to start the process!\
								 Sorry! Please click Try Again!'
				flash(danger_str,'danger')
				return render_template('fail.html', title='Ooops')

			# duplicates repo
			success_repo = github.duplicate_repo()
				
			# check if repo was successfully duplicated or not and display a message 
			if success_repo:
				username = github.user.username
				repo = github.user.repo
				success_str = 'Successful Repo Duplication! Thanks!'
				flash(success_str,'success')

				return render_template('thanks.html', title='Thanks', username=username, repo=repo)		

			else: # Fail duplicating repo
				danger_str = 'Failure duplicating the repo! Sorry! Please Try Again!'
		
		else: # No code received
			danger_str = 'Ooops Github did not send a code to start the process or\
							you got here the wrong way! Sorry! Please click Try Again!'

	else: # No GET request made
		danger_str = 'This page only processes GET requests with a valid code from Github for an OAuth app!'
		
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


# To run in command line
if __name__ == '__main__':
	app.run()
