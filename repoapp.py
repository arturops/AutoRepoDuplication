
# Web application to automatically duplicate a github repository 
# from one account to another
# To run for first time need to add an environment variable

# Linux, MacOSX: $ export FLASK_APP=AutoRepoDuplication.py
# Windows: $ set FLASK_APP=AutoRepoDuplication.py

from flask import Flask, render_template, url_for, flash, redirect, request
from forms import GithubUserForm
import apiwrap
import os
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = '2aba1f6ebe92e925ec34c8486003cf08'


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/about')
def about():
	version = {
		'author' : 'Arturo Parrales Salinas',
		'title' : 'Auto Repo Duplication App',
		'ver' : '0.0.0.1',
		'date' : 'June 25, 2018'
	}

	if request.method == 'GET':
		success_str = 'Repo has been created! Thanks!'
		flash(success_str,'success')
		print(request)
		print('\n\n{}\n\n'.format(request.args))


	return render_template('about.html', title='About', version=version)


@app.route('/access',methods=['GET','POST'])
def access():
	form = GithubUserForm()
	if form.validate_on_submit():
		
		repo = 'https://github.com/{}/{}'.format(form.github_username.data, form.target_repo.data)
		success_str = 'Repo {} has been created! Thanks {}!'.format(repo,form.github_username.data)
		flash(success_str,'success')
		flash(repo,'success')

		apiwrap.test()
		#r = requests.get('https://github.com/login/oauth/authorize?client_id=f7e621c81a2485a4bc70')
		#print('\n\n{}\n{}\n'.format(r.url,r))
		return redirect('https://github.com/login/oauth/authorize?client_id=f7e621c81a2485a4bc70')

		return redirect(url_for('home'))
	return render_template('access.html',title='User', form=form)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404





@app.route('/list')
def list():
	os.system('mkdir temp')
	f = []
	for root, dirs, files in os.walk("."):
		for folder in dirs:
			if folder == 'temp':
				print('Removing temp folder')
				os.system('rm -r temp')
		for file in files:
			print(file)
			f.append(file)
	f.append("Done")
	return '<h1>{}</h1><br /><h2>{}</h2>'.format(f[0],f[-1])

# To run in debug mode
if __name__ == '__main__':
	app.run(debug=True)
