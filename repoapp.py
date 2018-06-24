
# Web application to automatically duplicate a github repository 
# from one account to another
# To run for first time need to add an environment variable

# Linux, MacOSX: $ export FLASK_APP=AutoRepoDuplication.py
# Windows: $ set FLASK_APP=AutoRepoDuplication.py

from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
	return "<h1>Hello Arturo!!</h1>"


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
