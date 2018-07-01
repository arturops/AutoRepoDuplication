
import requests
import base64
import json

class APIuser():

	INVALID_TOKEN = 'Unknown'

	def __init__(self):
		"""
		APIuser class constructor

		Parameters:
			None

		Returns:
			None
		"""
		self.username = ''
		self.__token = INVALID_TOKEN


	def set_token(token):
		"""
		Helper function to set a user's access token 

		Parameters:
			token : User's access token

		Returns:
			None
		"""
		self.__token = token


	def get_token():
		"""
		Helper function to get a previously stored user's access token 

		Parameters:
			None

		Returns:
			__token : User's access token
		"""
		return self.__token


class API():


	def __init__(self, debug):
		"""
		API class constructor

		Parameters:
			debug : If True, the code will print to stdin HTTP packets, URL's and
					valuable important debug information

		Returns:
			None
		"""
		self.debug = debug
		self.user = APIuser()

	def APIerror(message):
		"""
		Prints in stdin the error of the API

		Parameters:
			message : String with a message to be printed on the stdin

		Returns:
			None
		"""
		print(message)


class GithubAPI(API):

	# Class Object Attributes

	GITHUB_API = 'https://api.github.com/'
	GITHUB_OAUTHS = 'https://github.com/login/oauth/authorize'
	GITHUB_TOKEN = 'https://github.com/login/oauth/access_token'


	GITHUB_USER_REPOS = 'https://api.github.com/user/repos'
	GITHUB_REPOS = 'https://api.github.com/repos/'

	TARGET_REPO_NAME = 'repotest' #'AutoRepoDuplication'
	ORIGIN_REPO_NAME = 'AutoRepoDuplication'

	def __init__(self, debug=False, client_app_info):
		"""
		GithubAPI class inherited from the API class
		GithubAPI class constructor

		Parameters:
			debug : Parameter passed to parent class API. If True, enables the stdin to output debug data
			client_app_info : Dictionary that contains the Github OAuths App information in the form: 
							{'client_id': GITHUB_CLIENT_ID, 'client_secret' : GITHUB_CLIENT_SECRET}

		Returns:
			None
		"""
		API.__init__(debug)
		self.client_app_info = client_app_info


	def __github_url(path):
		"""
		Builds a valid github URL by appending the give path to the standard Github API 

		Parameters:
			path : Path to append to the Github API. Must not stant with a '/' front slash.
			
		Returns:
			String of the URL created

		Example: 
			path = 'zen'
			return 'https://api.github.com/zen'
		"""
		return GITHUB_API + path


	def __get_github_motto():
		"""
		Test function to connect to the API and ensure Github replies with one of the phrases		

		Parameters:
			None

		Returns:
			String with Github's phrase
		"""
		r = requests.get(self.__github_url('zen'))
		if r.status_code >= 400:
			# Error
			APIerror('GET /zen {}'.format(resp.status_code))
		return str(r.content)


	def testAPI():
		"""
		Displays in stdin a phrase from the selection of Github's list. Uses __get_github_motto

		Parameters:
			None

		Returns:
			None
		"""
		print('Github phrase:\n\t\t \"{}\"'.format(self.__get_github_motto()))


	def check_payload(payload):
		if self.debug:
			print(payload)
		return

	def check_response(method, payload='None', url, response, success_code=None, task_message='' ):
		"""
		Print on the stdout the payload in the request, the type of request and, the response URL, the status 
		of the response and the content.

		Parameters:
			method : String describing the method used for the HTTP request: POST, GET, PUT, DELETE, PATCH, ... 
			payload : If there was payload in the HTTP request, one can eb passed to be printed, else it will
						will be displayed as 'None'
			url : the url of the HTTP request
			response : the response from the HTTP request
			success_code : The expected success code returned by the response
							Default value is None
			task_message : A message to display to describe the task done with the request
								Default value is ''

		Returns:
			None
		"""
		print('\n\n--------------------------- {} {} --------------------------- '.format(method, url))
		print('\nPayload: {}'.format(payload))
		print('\nResponse status code: {}'.format(response.status_code))
		print('\nResponse URL: {}'.format(response.url))
		print('\nResponse content:\n{}'.format(response.text))

		if success_code != None : 
			if response.status_code == success_code:
				print('\n------- SUCCESS {} ------- '.format(task_message))
			else:
				print('\n------- FAILED {} ------- '.format(task_message))

		return


	def get_github_auth_url(scope='public_repo'):
		"""
		Builds the Github auhorization URL

		Parameters:
			scope : Github scope(s) of the requested authorization on the user's github. Default is 'public_repo'b
					A list of github scopes can be found here:
					https://developer.github.com/apps/building-oauth-apps/understanding-scopes-for-oauth-apps/

		Returns:
			URL for the login website of Github to give an app authorization
		"""
		url = '{}?client_id={}&scope={}'.format(GITHUB_OAUTHS, self.client_app_info['client_id'], scope)
		return url


	def get_auth(code):
		"""
		Exchanges the code given by Github for an access token to a user's Github. The code is given after Github
		redirects the user to the app specified website once authorization was completed.

		The token is stored in the APIuser.__token member variable. This access token allows an OAuth app to access
		to a user's Github within the authorized scope.
		NOTE: This token is used instead of a user's username and password.

		Parameters:
			code : Github's given code after authorization is completed

		Returns:
			True if the token was retrieved, otherwise False

		"""
		#payload = client
		#payload['code'] = code

		# creates the parameters to ask for the access_token
		params = self.client_app_info
		params['code'] = code

		r = requests.post(GITHUB_TOKEN, params=params)

		# init token
		#token = 0

		if r.status_code >= 400:
			# Error
			APIerror('POST {} \nStatus Code: {}'.format(GITHUB_TOKEN, r.status_code))
		else:
			# parse the response for the access_token
			token_list = r.text.split('&')
			token = token_list[0].split('=')[1]
			self.user.set_token( token )

		if self.debug:
			check_response('POST', params, GITHUB_TOKEN, r)

			#print(self.user.get_token())
			if self.user.get_token() != self.user.INVALID_TOKEN:
				print('\n------- SUCCESS getting the token!! ------- ')
			else:
				print('\n------- FAILED getting the token!! ------- ')

		if self.user.get_token() != self.user.INVALID_TOKEN:
			return True
		else:
			return False


	def create_repo(repo_name=TARGET_REPO_NAME):
		"""
		Creates a public repository in the user's Github. REQUIRES to have a VALID user's TOKEN
		For more details: https://developer.github.com/v3/repos/#create

		Parameters:
			repo_name : Name of the public repository to create in the user's Github
			NOTE: Default value is TARGET_REPO_NAME from the GithubAPI class

		Returns:
			True if the repo is created successfully, otherwise False
		"""

		url = self.__github_url('user/repos')

		# Authorization Header
		headers = {'Authorization': 'token {}'.format(self.user.get_token())}

		# Payload
		data = { 	'name' : repo_name,
						'description': 'AutoRepoDuplication web app',
						'auto_init' : True, # adds README so that it generates an initial commit
						'private' : False # public repo
					}

		r = requests.post(url,headers=headers, json=data)
		
		if self.debug:
			check_response('POST', data, url, r, 201, ' creating repo!! ')

		if r.status_code == 201: 
			return True
		else:
			return False


	def get_HEADreference(owner, repo_name=TARGET_REPO_NAME, branch='master'):
		"""
		Retrieves the HEAD reference of the repo_name given and the branch parameter passed. 
		NOTE: 	Default branch is master. 
				Default repo_name is the TARGET_REPO_NAME from GithubAPI class
		
		For more details: https://developer.github.com/v3/git/refs/#get-a-reference

		Parameters:
			repo_name : Name of the repository to find the reference from in the user's Github
			NOTE: Default value is TARGET_REPO_NAME from the GithubAPI class

			branch: Branch in the repo_name to find the reference from in the user's Github
			NOTE: Default branch is master. 

		Returns:
			branch_url : Github's url where the branch reference is located
			branch_sha : SHA of the branch
		"""
		
		owner_repo_refs = owner + '/'+ repo_name + '/git/refs/heads/' + branch 
		url = self.__github_url('user/repos'+owner_repo_refs) #GITHUB_REPOS+owner_repo_refs

		headers = { 'Authorization' : 'token {}'.format(self.user.get_token())}

		r = requests.get(url, headers=headers)

		if r.status_code == 201: 
			# parse response for object url and sha
			rjson = r.json()
			branch_url, branch_sha = rjson['object']['url'],rjson['object']['sha']
		else:
			branch_url, branch_sha = '',''

		
		if self.debug:
			if r.status_code == 201: 
				print('\nreference URL: {}\nreference SHA: {}\n'.format(branch_url, branch_sha))

			check_response('GET', 'None', url, r, 201, ' retrieving reference!! ')


		return branch_url, branch_sha



	def get_commit(commit_reference_url):
		"""
		Retrieves a commit's reference tree of the given url. 
		For more details: https://developer.github.com/v3/git/commits/#response

		Parameters:
			commit_reference_url : URL reference from which to retrieve a tree

		Returns:
			tree_url : Github's url where the tree reference is located
			tree_sha : SHA of the tree
		"""

		r = requests.get(commit_reference_url)
		
		if r.status_code == 200: 
			tree_url, tree_sha = r.json()['tree']['url'],r.json()['tree']['sha']
		else:
			tree_url, tree_sha = '',''


		if self.debug:
			if r.status_code == 200: 
				print('\ntree reference URL: {}\ntree reference SHA: {}\n'.format(tree_url, tree_sha))

			check_response('GET', 'None', commit_reference_url, r, 200, ' retrieving tree reference!! ')
			
		return tree_url, tree_sha


	def get_file_content(path, file):
		"""
		Retrieves the content of a file 

		Parameters:
			path : path where the file is stored
			file : Filename to retrieve the content

		Returns:
			content : Content of the file
		"""
		with open(path+file, 'r') as content_file:
			content = content_file.read()
		return content


	def create_blob(owner, repo_name = TARGET_REPO_NAME, file_path, file, return_content=True):
		"""
		Retrieves the content of a file and generates a SHA and a blob 
		For more details: https://developer.github.com/v3/git/blobs/#create-a-blob
		NOTE: The Github API supports blobs up to 100 megabytes in size.

		Parameters:
			owner : The username of the user
			repo_name : The name of the repo in which the blobs will be stored
						Default value is TARGET_REPO_NAME from GithubAPI class
			file_path : path where the file to convert in a blob is locally stored
			file : file to convert in a blob
			return_content: This boolean allows the function to return the content of the file
							that was converted in a blob. This is useful when adding new files to a 
							repository, as its content must be added instead of SHA.
							Default value is True

		Returns:
			sha: SHA of the blob
			
			If return_content is True, it also returns the file's content used to generate the blob's SHA
				content : Content of the file
		"""
		
		url = self.__github_url('repos/{}/{}/git/blobs'.format(owner,repo_name)) 
		#GITHUB_API + 'repos/{}/{}/git/blobs'.format(owner,repo)

		content =  get_file_content(file_path, file)
		

		headers = { 'Authorization' : 'token {}'.format(self.user.get_token())}
		
		#python source code is utf-8 by default, so no need to encode it
		payload = { "content": content,
					"encoding": "utf-8" }

		
		r = requests.post(url, headers=headers, json=payload)

		sha = ''
		if r.status_code == 201:
			sha = r.json()['sha']

		if self.debug:
			if r.status_code == 201: 
				print('Blob SHA {}'.format(sha))

			check_response('POST', payload, url, r, 201, ' creating blob!! ')

		
		if return_content:
			return sha, content
		else:
			return sha


	def get_target_tree(owner, repo_name=ORIGIN_REPO_NAME, tree_sha, recursive_tree=True):
		"""
		Retrieves a tree from an owner, repo_name and the tree SHA. The retrieval can be non-recursive which will 
		not return files in nested trees, or it can be recursive and return also the nested trees.
		For more details: https://developer.github.com/v3/git/trees/#get-a-tree
		

		Parameters:
			owner : The username from which to get the tree
			repo_name : The name of the repo from which to read the tree
						Default value is ORIGIN_REPO_NAME from GithubAPI class
			tree_sha : SHA of the tree to retrieve
			recursive_tree : If True returns the nested trees and blobs.
						Default value is True

		Returns:
			tree : the tree structure
		"""
		
		url = self.__github_url('repos/{}/{}/git/trees/{}'.format(owner,repo,tree_sha))

		params = {'recursive' : 1}

		if recursive_tree:
			r = requests.get(url, params=params)
		else:
			r = requests.get(url)

		tree = ''
		if r.status_code == 200:
			tree = r.json() # tree = json.loads(r.text)
			
			# cleaning the response tree
			del tree['url']
			del tree['truncated']
			# remove any tree element, it will be infered by the 'path' of blobs
			tree['tree'][:] = [item for item in tree['tree'] if item['type'] != 'tree']
			
			# clean blobs
			for element in tree['tree']:
				if element['mode'] == '100644': #BLOB type has mode 100644
					del element['size']
				#else is a tree and has no size, but has url
				del element ['url']


		if self.debug:

			if r.status_code == 200:
				print('\n-------------------- TARGET TREE TO POST --------------------------------\n')
				print(tree)
				print('\n-------------------------------------------------------------------------\n')

			check_response('GET', params, url, r, 200, 'retrieving target tree !! ')

		return tree


	def create_tree(owner, tree, repo_name=TARGET_REPO_NAME, base_tree=None):
		"""
		Posts a tree in the user's Github desired repo and gets a response of the posted tree structure 
		and its SHA of such tree
		For more details: https://developer.github.com/v3/git/trees/#create-a-tree
		

		Parameters:
			owner : The username from which to get the tree
			tree : The tree structure to post
			repo_name : The name of the repo from which to read the tree
						Default value is TARGET_REPO_NAME from GithubAPI class
			base_tree: The tree to which this other tree will be appended (if any, otherwise leave it empty)
						Default value is None

		Returns:
			posted_tree_sha : the SHA of the posted tree structure
		"""
		
		url = self.__github_url('repos/{}/{}/git/trees'.format(owner,repo))
		#GITHUB_API+ 'repos/{}/{}/git/trees'.format(owner,repo)
		
		headers = { 'Authorization' : 'token {}'.format(self.user.get_token())}

		if base_tree == None:
			payload = { 'tree' : tree }
		else:
			payload = { 'base_tree' : base_tree,
						'tree' : tree }


		r = requests.post(url, headers=headers, json=payload)

		posted_tree_sha = None
		if r.status_code == 201:
			posted_tree_sha	= r.json()['sha']

		if self.debug:
			check_response('POST', payload, url, r, 201, ' posting the tree !!')

		return posted_tree_sha


	def create_commit(new_tree_sha, owner, repo_name=TARGET_REPO_NAME, HEAD_tree_sha=None ):
		"""
		Creates a new commit in the user's Github desired repo in order to commit a previously posted tree. 
		It requires the SHA of the posted tree to commit.
		For more details: https://developer.github.com/v3/git/commits/#create-a-commit 
		

		Parameters:
			new_tree_sha: The SHA of the previously posted tree  
			owner : The username
			tree : The tree structure to post
			repo_name : The name of the repo in which to commit the tree
						Default value is TARGET_REPO_NAME from GithubAPI class
			HEAD_tree_sha: The HEAD tree to which this other tree will be appended (if any, otherwise leave it empty)
						Default value is None

		Returns:
			commit_sha : the SHA of the commit
		"""
		
		url = self.__github_url('repos/{}/{}/git/commits'.format(owner, repo))
		#GITHUB_API+'repos/{}/{}/git/commits'.format(owner, repo)

		parents = []
		if HEAD_tree_sha != None:
			parents.append(HEAD_tree_sha)


		payload = {	"message": "Auto Repo Duplication code of flask web app from API",
					"author": {
	    						"name": "Arturo Parrales",
	    						"email": "arturo.ps14@gmail.com",
	    						"date": "2018-06-30T09:13:30+12:00"
	    						},
	    			"parents": parents,
	    			"tree": new_tree_sha
	    			}


		headers = { 'Authorization' : 'token {}'.format(self.user.get_token())}
		
		r = requests.post(url, headers=headers, json=payload)

		commit_sha = None
		if r.status_code == 201:
			commit_sha = r.json()['sha']

		if self.debug:
			print('\nCommit SHA: {}'.format(commit_sha))
			check_response('POST', payload, url, r, 201, ' creating commit !! ')		

		return commit_sha



	def update_reference(owner, repo, reference, new_sha, force_update=True):
		#https://developer.github.com/v3/git/refs/#update-a-reference

		url = GITHUB_API+'repos/{}/{}/git/refs/{}'.format(owner, repo, reference)
		payload = { 'sha' : new_sha, 
					'force' : force_update}
		token = '8a5f3ffdc47142562f00dc016bacadb0cfbf539d'
		headers = { 'Authorization' : 'token {}'.format(token)}

		r = requests.patch(url, headers=headers, json=payload)

		print('\nUpdate REFERENCE ------- \n')
		print(r)
		print(r.text)
		print('--------------------------------------------')
		print(r.json())

		if r.status_code == 200:
			return	True
		else:
			return False 

#--------------------------- maybe not used at all -----------------
	check_response(method, payload='None', url, response, success_code=None, task_message='' )


	def get_github_auth_url(scope='public_repo'):
		"""
		Builds the Github auhorization URL

		Parameters:
			scope : scopes of the requested authorization on the user's github
					A list of github scopes can be found here:
					https://developer.github.com/apps/building-oauth-apps/understanding-scopes-for-oauth-apps/

		Returns:
			URL for the login website of Github to give an app authorization
		"""
		url = '{}?client_id={}&scope={}'.format(GITHUB_OAUTHS, client['client_id'], 'public_repo')
		return url


client = { 'client_id':'f7e621c81a2485a4bc70',
			'client_secret':'fe67f77d4b2c56a38e7e99cc2d6b0720e6b4d4d0'
}

github = GithubAPI(debug=True, client)





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




def list_repo(token):
	url = GITHUB_USER_REPOS
	headers = {'Authorization': 'token {}'.format(token)}
	r = requests.get(url, headers=headers)
	print(r)
	print('\n\n{}\n\n'.format(r.json()))
	return True






def get_tree_by_url(tree_url):
	#https://developer.github.com/v3/git/trees/#get-a-tree
	print(tree_url)
	r = requests.get(tree_url)
	print(r)
	print(r.json())
	return

def get_tree_by_sha(owner,repo, tree_sha, recursive_tree=True):
	#https://developer.github.com/v3/git/trees/#get-a-tree
	tree_url = GITHUB_API + 'repos/{}/{}/git/trees/{}'.format(owner,repo,tree_sha)
	if recursive_tree:
		tree_url = GITHUB_API + 'repos/{}/{}/git/trees/{}?recursive=1'.format(owner,repo,tree_sha)
	print(tree_url)
	r = requests.get(tree_url)
	print(r)
	print(r.json())
	print('\n------------------------------------------------------\n')
	print(r.text.replace('arturops/AutoRepoDuplication','xxx/repotest'))
	r2 = json.loads(r.text)
	print('\n------------------------------------------------------\n')
	print(r2)
	print(type(r2))
	sha = r.json()['sha']
	sha2 = r2['sha']
	print(sha == sha2)
	return sha








def try_commit():
	owner = 'arturops'
	repo = 'AutoRepoDuplication'
	# get reference HEAD points to
	branch_url, branch_sha = get_HEADreference('x', owner, repo, branch='master')
	# get tree HEAD points to
	HEAD_tree_url, HEAD_tree_sha = get_commit(branch_url)
	file_path = ''
	file = 'autorepo.py'
	#blob_sha = create_blob(owner, repo, file_path, file, False)
	blob_sha = '4aa5f1111a60e3db06877304e58ed76dc673e2af'
	#get_tree_by_url(HEAD_tree_url)
	#get_tree_by_sha(owner,repo, HEAD_tree_sha)
	target_tree = get_target_tree(owner,repo, HEAD_tree_sha, recursive_tree=True)
	expected_tree_sha = target_tree['sha']
	new_tree = target_tree['tree']

	
	owner = 'arturops'
	repo = 'repotest'
	# get reference HEAD points to
	branch_url, branch_sha = get_HEADreference('x', owner, repo, branch='master')
	# get tree HEAD points to
	HEAD_tree_url, HEAD_tree_sha = get_commit(branch_url)

	# convert new_tree into a valid new_tree [need to swap sha for content as it is the first commit of these files]
	post_tree = []
	for item in new_tree:
		if item['mode'] == '100644':
			file_path = item['path']
			blob_sha, blob_content = create_blob(owner, repo, file_path, '')
			if blob_sha != item['sha']:
				print('\n**********  FILE: {} does NOT have SAME SHA as tree !  ***********\n'.format(file_path))
			del item['sha']
			item['content'] = blob_content
			post_tree.append(item)

	print('\n------------- NEW TREE ------------------------')
	for i in new_tree:
		print(i['type'], i['path'] )
	print()
	print('\n------------- POST TREE ------------------------')
	for i in post_tree:
		print(i['type'], i['path'] )
	print()

	# post new tree
	new_tree_sha = create_tree(owner, repo, HEAD_tree_sha, post_tree)

	print('Expected sha = new sha ? {}'.format(expected_tree_sha==new_tree_sha))

	# create a commit for the tree
	commit_sha = create_commit(owner, repo, HEAD_tree_sha, new_tree_sha)

	reference = 'heads/master'

	success = update_reference(owner, repo, reference, commit_sha)

	if success:
		print(' ----------------- SUCCESS --------------------')

	return




def test():
	get_github_motto()



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


