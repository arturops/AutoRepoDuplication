
import requests
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
		self.__token = self.INVALID_TOKEN


	def set_token(self, token):
		"""
		Helper function to set a user's access token 

		Parameters:
			token : User's access token

		Returns:
			None
		"""
		self.__token = token


	def get_token(self):
		"""
		Helper function to get a previously stored user's access token 

		Parameters:
			None

		Returns:
			__token : User's access token
		"""
		return self.__token

class GithubAPIuser(APIuser):

	USER_TARGET_REPO_NAME = 'repotest' #'AutoRepoDuplication'
	USER_ORIGIN_REPO_NAME = 'AutoRepoDuplication'

	def __init__(self, repo=USER_ORIGIN_REPO_NAME ):
		"""
		GithubAPIuser class constructor

		Parameters:
			None

		Returns:
			None
		"""
		APIuser.__init__(self)
		self.repo = repo




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
		

	def APIerror(self, message):
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

	TARGET_REPO_NAME = 'AutoRepo'
	ORIGIN_REPO_NAME = 'AutoRepoDuplication'

	def __init__(self, debug=False):
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
		API.__init__(self, debug=debug)
		
		# read owner_info
		with open('owner_info.txt') as json_file:
			owner_info = json.load(json_file)

		self.user = GithubAPIuser(owner_info['user']['repo'])
		self.user.username = 'Unknownn' #Extracted after authorization token is obtained

		
		self.owner = GithubAPIuser(owner_info['owner']['repo'])
		self.owner.username = owner_info['owner']['username'] # ingested from owner_info file
		self.client_app_info = owner_info['app'] # ingested from owner_info file


	def __github_url(self, path):
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
		return self.GITHUB_API + path


	def __get_github_motto(self):
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
			self.APIerror('GET /zen {}'.format(resp.status_code))
		return str(r.text)


	def testAPI(self):
		"""
		Displays in stdin a phrase from the selection of Github's list. Uses __get_github_motto

		Parameters:
			None

		Returns:
			None
		"""
		print('Github phrase:\n\t\t \"{}\"'.format(self.__get_github_motto()))


	def check_response(self, method, url, response, payload='None', success_code=None, task_message='' ):
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


	def get_github_auth_url(self, scope='public_repo'):
		"""
		Builds the Github auhorization URL

		Parameters:
			scope : Github scope(s) of the requested authorization on the user's github. Default is 'public_repo'b
					A list of github scopes can be found here:
					https://developer.github.com/apps/building-oauth-apps/understanding-scopes-for-oauth-apps/

		Returns:
			URL for the login website of Github to give an app authorization
		"""
		url = '{}?client_id={}&scope={}'.format(self.GITHUB_OAUTHS, self.client_app_info['client_id'], scope)
		return url


	def get_auth(self, code):
		"""
		Exchanges the code given by Github for an access token to a user's Github. The code is given after Github
		redirects the user to the app specified website once authorization was completed.

		This access token allows an OAuth app to access to a user's Github within the authorized scope.
		
		Parameters:
			code : Github's given code after authorization is completed

		Returns:
			token : the token that was retrieved
					NOTE: This token is used instead of a user's username and password, so treated like a password

		"""

		# creates the parameters to ask for the access_token
		params = self.client_app_info
		params['code'] = code

		r = requests.post(self.GITHUB_TOKEN, params=params)

		# init token
		token = None
		if r.status_code >= 400:
			# Error
			self.APIerror('POST {} \nStatus Code: {}'.format(self.GITHUB_TOKEN, r.status_code))
		else:
			# parse the response for the access_token
			token_list = r.text.split('&')
			token = token_list[0].split('=')[1]
			

		if self.debug:
			self.check_response('POST', self.GITHUB_TOKEN, r, params)

			if token:
				print('\n------- SUCCESS getting the token!! ------- ')
			else:
				print('\n------- FAILED getting the token!! ------- ')

		return token 


		if self.user.get_token() != self.user.INVALID_TOKEN:
			return True
		else:
			return False


	def create_repo(self, repo_name=TARGET_REPO_NAME):
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
			self.check_response('POST', url, r, data, 201, ' creating repo!! ')

		if r.status_code == 201: 
			return True
		else:
			return False


	def get_HEADreference(self, owner, repo_name=TARGET_REPO_NAME, branch='master', token=None):
		"""
		Retrieves the HEAD reference of the repo_name given and the branch parameter passed. 
		NOTE: 	Default branch is master. 
				Default repo_name is the TARGET_REPO_NAME from GithubAPI class
		
		For more details: https://developer.github.com/v3/git/refs/#get-a-reference

		Parameters:
			owner : The username of the user
			repo_name : Name of the repository to find the reference from in the user's Github
			NOTE: Default value is TARGET_REPO_NAME from the GithubAPI class

			branch: Branch in the repo_name to find the reference from in the user's Github
			NOTE: Default branch is master. 

			token : access token to give authorization

		Returns:
			branch_url : Github's url where the branch reference is located
			branch_sha : SHA of the branch
		"""
		
		owner_repo_refs = owner + '/'+ repo_name + '/git/refs/heads/' + branch 
		url = self.__github_url('repos/'+owner_repo_refs) 

		headers = { 'Authorization' : 'token {}'.format(token)}


		if token:
			r = requests.get(url, headers=headers)
		else:
			r = requests.get(url, params=self.client_app_info)

		if r.status_code == 200: 
			# parse response for object url and sha
			rjson = r.json()
			branch_url, branch_sha = rjson['object']['url'],rjson['object']['sha']
		else:
			branch_url, branch_sha = None, None

		
		if self.debug:
			if r.status_code == 200: 
				print('\nreference URL: {}\nreference SHA: {}\n'.format(branch_url, branch_sha))

			self.check_response('GET', url, r, 'None', 200, ' retrieving reference!! ')

		return branch_url, branch_sha



	def get_commit(self, commit_reference_url, token=None):
		"""
		Retrieves a commit's reference tree of the given url. 
		For more details: https://developer.github.com/v3/git/commits/#response

		Parameters:
			commit_reference_url : URL reference from which to retrieve a tree
			token : access token of a user. Default is None as this call does not required a token

		Returns:
			tree_url : Github's url where the tree reference is located
			tree_sha : SHA of the tree
		"""

		headers = { 'Authorization' : 'token {}'.format(token)}

		if token:
			r = requests.get(commit_reference_url, headers=headers)
		else:
			r = requests.get(commit_reference_url, params=self.client_app_info)
		
		
		if r.status_code == 200: 
			tree_url, tree_sha = r.json()['tree']['url'],r.json()['tree']['sha']
		else:
			tree_url, tree_sha = '',''


		if self.debug:
			if r.status_code == 200: 
				print('\ntree reference URL: {}\ntree reference SHA: {}\n'.format(tree_url, tree_sha))

			self.check_response('GET', commit_reference_url, r, 'None', 200, ' retrieving tree reference!! ')
			
		return tree_url, tree_sha


	def get_file_content(self, path, file):
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


	def create_blob(self, owner, file_path, file, repo_name = TARGET_REPO_NAME, return_content=True):
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

		content =  self.get_file_content(file_path, file)
		

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

			self.check_response('POST', url, r, payload, 201, ' creating blob!! ')

		
		if return_content:
			return sha, content
		else:
			return sha


	def get_target_tree(self, owner, tree_sha, repo_name=ORIGIN_REPO_NAME, recursive_tree=True):
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
		
		url = self.__github_url('repos/{}/{}/git/trees/{}'.format(owner,repo_name,tree_sha))

		params = {'recursive' : 1}

		if recursive_tree:
			r = requests.get(url, params=params)
		else:
			params = self.client_app_info
			params['recursive'] = 1
			r = requests.get(url, params=params)

		tree = ''
		tree_clean = []
		if r.status_code == 200:
			tree = r.json() # tree = json.loads(r.text)
			
			# cleaning the response tree
			del tree['url']
			del tree['truncated']
			
			# remove any tree element, it will be infered by the 'path' of blobs
			# remove also the owner_info file so that credentials are not distributed to next users
			#tree['tree'][:] = [item for item in tree['tree'] if item['type'] != 'tree'\
			#												 and item['path'] != 'owner_info.txt']
			# clean blobs
			for element in tree['tree']:
				if element['type'] != 'tree' and element['path'] != 'owner_info.txt' and \
				element['mode'] == '100644': #BLOB type has mode 100644
					del element['size']
					#else is a tree and has no size, but has url
					del element ['url']
					tree_clean.append(element)

			tree['tree'] = tree_clean

		if self.debug:

			if r.status_code == 200:
				print('\n-------------------- TARGET TREE TO POST --------------------------------\n')
				print(tree)
				print('\n-------------------------------------------------------------------------\n')

			self.check_response('GET', url, r, params, 200, 'retrieving target tree !! ')

		return tree


	def convert_to_content_tree(self, tree):
		"""
		Convert a given tree structure that contains only the blobs SHA's into a valid content_tree. The 
		content tree will use the content field in the HTTP request to add new blobs.
		This new tree will be posted/created into the user's github repo.
		In summary, it swaps SHA's for actual file content. This is required for the first commit of files.

		Parameters:
			tree : the tree to convert into a content tree

		Returns:
			content_tree : A tree that has removed SHA field for Content fields

		"""
		
		content_tree = []
		for item in tree:
			if item['mode'] == '100644':
				file_path = item['path']
				blob_sha, blob_content = self.create_blob(self.user.username, file_path, '', self.user.repo)
				if self.debug and blob_sha != item['sha']:
					print('\n**********  FILE: {} does NOT have SAME SHA as tree !  ***********\n'.format(file_path))
				del item['sha']
				item['content'] = blob_content
				content_tree.append(item)

		return content_tree


	def create_tree(self, owner, tree, repo_name=TARGET_REPO_NAME, base_tree=None):
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
		
		url = self.__github_url('repos/{}/{}/git/trees'.format(owner,repo_name))
		
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
			self.check_response('POST', url, r, payload, 201, ' posting the tree !!')

		return posted_tree_sha


	def create_commit(self, new_tree_sha, owner, repo_name=TARGET_REPO_NAME, HEAD_tree_sha=None ):
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
		
		url = self.__github_url('repos/{}/{}/git/commits'.format(owner, repo_name))

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
			self.check_response('POST', url, r, payload, 201, ' creating commit !! ')		

		return commit_sha



	def update_reference(self, owner, reference, new_commit_sha, repo_name=TARGET_REPO_NAME, force_update=True):
		"""
		Updates the reference of a commit in the github repository, so that it reflects the changes in the repo.
		It requires the SHA of the new commit.
		For more details: https://developer.github.com/v3/git/refs/#update-a-reference
		
		Parameters:
			owner : The username
			reference: the reference branch to which to update the commit
			new_commit_sha: The SHA of the new commit 
			repo_name : The name of the repo in which to commit
						Default value is TARGET_REPO_NAME from GithubAPI class
			force_update: Defines if the update will be forced or if it is a fast forward update.
						Default value is True

		Returns:
			True if the update was succesful, otherwise it returns False
		"""

		url = self.__github_url('repos/{}/{}/git/refs/{}'.format(owner, repo_name, reference))

		payload = { 'sha' : new_commit_sha, 
					'force' : force_update}

		headers = { 'Authorization' : 'token {}'.format(self.user.get_token())}

		r = requests.patch(url, headers=headers, json=payload)

		if self.debug:
			self.check_response('PATCH', url, r, payload, 200, ' updating reference !! ' )

		if r.status_code == 200:
			return	True
		else:
			return False 


	def get_user_username(self):
		"""
		Retrieves the username of a user that has given the app an authorization 
		For more details: https://developer.github.com/v3/users/#get-the-authenticated-user

		Parameters:
			None

		Returns:
			True if it was able to get a succesful response from which it got the username

		"""
		url = self.__github_url('user')

		headers = { 'Authorization' : 'token {}'.format(self.user.get_token())}

		r = requests.get(url, headers=headers)

		if r.status_code == 200:
			self.user.username = r.json()['login']
			return True
		else:
			return False


	def duplicate_repo(self, code, origin_branch='master', target_branch='master'):
		"""
		Uses several methods from the GithubAPI class to copy a repo from an owner to the user that
		authorize the app.

		Parameters:
			code : is a code that Github returns after a user authorized the app access to his/her github
			origin_branch : is the branch of the owner that will be copied
			target_branch : is the branc of the user in which the owner repo will be copied

		Returns:
			True if it the update reference was succesful, which will imply the repo got copied soccessfully

		"""
		
		# Repo Owner 
		branch_url, branch_sha = self.get_HEADreference(self.owner.username, 
													self.owner.repo, origin_branch)
		HEAD_tree_url, HEAD_tree_sha = self.get_commit(branch_url) 
		target_tree = self.get_target_tree(self.owner.username, HEAD_tree_sha, self.owner.repo, recursive_tree=True)
		expected_tree_sha = target_tree['sha']
		expected_tree = target_tree['tree']


		# Get user/client token and create repo
		self.user.set_token( self.get_auth(code) )
		success = self.create_repo(self.user.repo) #think it should get token
		success = self.get_user_username()
 
		branch_url, branch_sha = self.get_HEADreference(self.user.username, 
													self.user.repo, target_branch,
													self.user.get_token())
		HEAD_tree_url, HEAD_tree_sha = self.get_commit(branch_url, self.user.get_token())
		content_tree = self.convert_to_content_tree(expected_tree)
		# post new tree
		posted_tree_sha = self.create_tree(self.user.username, content_tree, self.user.repo)
		print('Expected sha = new sha ? {}'.format(expected_tree_sha==posted_tree_sha))
		# create a commit for the tree
		commit_sha = self.create_commit(posted_tree_sha, self.user.username, self.user.repo)
		# update reference
		reference = 'heads/{}'.format(target_branch)
		success = self.update_reference(self.user.username, reference, commit_sha, self.user.repo, force_update=True)

		if success:
			print(' ----------------- SUCCESS --------------------')
			print('OWNER {}'.format(self.owner.username))
			print('USER {}'.format(self.user.username))

		return success


	def get_owner_repo_tree(self, origin_branch='master'):
		"""
		Retrieves a recursive tree from an owner repo.
		
		Parameters:
			origin_branch : is the branch of the owner that will be copied

		Returns:
			expected_tree : owner's repo tree
		"""
		# Repo Owner 
		branch_url, branch_sha = self.get_HEADreference(self.owner.username, 
													self.owner.repo, origin_branch)
		HEAD_tree_url, HEAD_tree_sha = self.get_commit(branch_url) 
		target_tree = self.get_target_tree(self.owner.username, HEAD_tree_sha,
											 self.owner.repo, recursive_tree=True)

		expected_tree = target_tree['tree']

		return expected_tree


	def commit_repo(self, code, expected_tree, target_branch='master'):
		"""
		Uses several methods from the GithubAPI class to commit a repo from an owner's tree to the user that
		authorize the app.

		Parameters:
			code : is a code that Github returns after a user authorized the app access to his/her github
			expected_tree: tree to commit to the repo
			target_branch : is the branc of the user in which the owner repo will be copied

		Returns:
			True if it the update reference was succesful, which will imply the repo got copied soccessfully

		"""
		# Get user/client token and create repo
		self.user.set_token( self.get_auth(code) )
		success = self.create_repo(self.user.repo)
		success = self.get_user_username()


		# Repo User/Client 
		branch_url, branch_sha = self.get_HEADreference(self.user.username, 
													self.user.repo, target_branch,
													self.user.get_token())
		HEAD_tree_url, HEAD_tree_sha = self.get_commit(branch_url, self.user.get_token())
		content_tree = self.convert_to_content_tree(expected_tree)
		# post new tree
		posted_tree_sha = self.create_tree(self.user.username, content_tree, self.user.repo)
		# create a commit for the tree
		commit_sha = self.create_commit(posted_tree_sha, self.user.username, self.user.repo)
		# update reference
		reference = 'heads/{}'.format(target_branch)
		success = self.update_reference(self.user.username, reference, commit_sha, self.user.repo, force_update=True)

		if success:
			print(' ----------------- SUCCESS --------------------')
			print('OWNER {}'.format(self.owner.username))
			print('USER {}'.format(self.user.username))

		return success










