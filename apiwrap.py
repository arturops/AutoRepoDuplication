
import requests
#from urlparse import urljoin

GITHUB_API = 'https://api.github.com/'
GITHUB_OAUTHS = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN = 'https://github.com/login/oauth/access_token'

client = { 'client_id':'f7e621c81a2485a4bc70',
			'client_secret':'fe67f77d4b2c56a38e7e99cc2d6b0720e6b4d4d0'
}

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


def get_auth(code):
	payload = client
	payload['code'] = code
	r = requests.post(GITHUB_TOKEN,params=payload)
	print(r)
	print('\n\n\n ------------------------------------------------------\n\n')
	print(r.url)
	print(r.text)
	print('\n\n\n -- \n\n')
	#print(r.__dict__)
	#token = str(r.__dict__['_content'])
	token_list = r.text.split('&')
	print(token_list)
	token = token_list[0].split('=')[1]
	print(token)
	#with open('test.html','w') as f:
	#	f.write(str(resp.content))
	if r.status_code >= 400:
		# Error
		raise ApiError('GET Authorizations {}'.format(r.status_code))
	#code = resp.json()['code']
	#print('\n\nCode: {}\n\n'.format(code))
	#print('{}'.format(resp.content))
	return token

def create_repo(token):
	url = 'https://api.github.com/user/repos'
	headers = {'Authorization': 'token {}'.format(token)}
	r = requests.get(url, headers=headers)
	print(r)
	print('\n\n{}\n\n'.format(r.__dict__))
	return


def run():
	username = 'arturops'
	get_github_motto()
	print()
	client_id = get_user_id(username)
	print('\n\nclient_id (main) :{}\n\n'.format(client_id))
	#token = get_user_auth(username)
	#print('\n\ntoken (main) :{}\n\n'.format(token))
	#client_id = 'f7e621c81a2485a4bc70'
	print('\n\nclient_id (github) :{}\n\n'.format(client_id))
	web_auth_str = get_auth(client_id)
	#web_auth_str = 'https://github.com/login/oauth/authorize?client_id={}'.format(client_id)
	return web_auth_str

#run()

def test():
	get_github_motto()





