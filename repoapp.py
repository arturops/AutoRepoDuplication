
# Web application to automatically duplicate a github repository 
# from one account to another


from flask import Flask, render_template, url_for, flash, redirect, request
from forms import GithubUserForm
import apiwrap


app = Flask(__name__)

app.config['SECRET_KEY'] = '2aba1f6ebe92e925ec34c8486003cf08'
app.config['DEBUG'] = False

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
	github = apiwrap.GithubAPI(debug=app.config['DEBUG'])
	return redirect('https://github.com/{}/{}'.format(github.owner.username, github.owner.repo))


@app.route('/access',methods=['GET','POST'])
def access():
	form = GithubUserForm()
	if form.validate_on_submit():

		github = apiwrap.GithubAPI(debug=app.config['DEBUG'])
		#print( github.testAPI() )
		return redirect(github.get_github_auth_url())

	return render_template('access.html',title='User', form=form)


@app.route('/done')
def done():

	username = ''
	repo = ''
	if request.method == 'GET':
		
		if 'code' in request.args:

			code = request.args['code']
			
			github = apiwrap.GithubAPI(debug=app.config['DEBUG'])
			success_repo = github.duplicate_repo(code)

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

# Handles Server Internal errors
@app.errorhandler(500)
def server_error(e):
	return render_template('500.html'),500


# To run in debug mode
if __name__ == '__main__':
	app.run()
