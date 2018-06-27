
import requests
#from urlparse import urljoin

GITHUB_API = 'https://api.github.com/'

def github_url(path):
	#return urljoin(GITHUB_API,path)
	return GITHUB_API + path

def get_github_motto():
	resp = requests.get(github_url('zen'))
	if resp.status_code >= 400:
		# Error
		raise ApiError('GET /zen {}'.format(resp.status_code))
	print('Github phrase:\n\t\t \"{}\"'.format(resp.content))

def get_user_id(username):
	resp = requests.get(github_url('users/' + username))
	#resp = requests.get('https://api.github.com/users/defunkt')
	if resp.status_code >= 400:
		# Error
		raise ApiError('GET /users/ {}'.format(resp.status_code))
	#for item in resp.json():
	print('{}'.format(resp.json()))
	client_id = resp.json()['id']
	print('client id: {}'.format(client_id))
	return client_id


def get_user_auth(username):
	json_params = {"scopes": ["repo", "user"], "note": "test"}
	resp = requests.post('https://api.github.com/authorizations/', json=json_params)
	if resp.status_code >= 400:
		# Error
		print(resp)
		print(resp.content)
		raise ApiError('GET Authorizations {}'.format(resp.status_code))
	print(resp)
	token = resp.json()['token']
	print('token: {}'.format(token))
	print('{}'.format(resp.content))
	return token


def get_auth(client_id):
	web_auth_str = 'https://github.com/login/oauth/authorize?client_id={}&redirect_uri={}&state={}'.format(client_id,'https://www.google.com','afghrsgdg')
	#web_auth_str = 'https://github.com/login/oauth/authorize?client_id={}'.format(client_id)
	resp = requests.get(web_auth_str)
	print(web_auth_str )
	print('\n\n\n ------------------------------------------------------\n\n')
	print(resp)
	#with open('test.html','w') as f:
	#	f.write(str(resp.content))
	if resp.status_code >= 400:
		# Error
		raise ApiError('GET Authorizations {}'.format(resp.status_code))
	#code = resp.json()['code']
	#print('\n\nCode: {}\n\n'.format(code))
	#print('{}'.format(resp.content))


def run():
	username = 'arturops'
	get_github_motto()
	print()
	client_id = get_user_id(username)
	print('\n\nclient_id (main) :{}\n\n'.format(client_id))
	#token = get_user_auth(username)
	#print('\n\ntoken (main) :{}\n\n'.format(token))
	get_auth(client_id)

#run()






