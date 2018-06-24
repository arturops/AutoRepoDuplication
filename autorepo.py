
# Script to create Github repo automatically

import os

USER = 'arturops'
REPO = 'AutoRepoDuplication'

github_new_repo_cmd = 'curl -u {} https://api.github.com/user/repos -d \'{{\"name\": \"{}\"}}\''.format(USER,REPO)


# creates github repo on the online platform
os.system(github_new_repo_cmd)

# makes current folder a github repo
os.system('git init')

# add to commit all python scripts if any
os.system('git add *.py')

# description of repo
REPO_DESCRIPTION = 'Created a new repository to develop a web application\
 that can auto duplicate its source code and documentation to a user\'s \
 github. The only anticipated requirements are that the user opens the URL\
  of such app and provides username and desired repo name'

# creates README file
os.system('echo \"# {}\" > README.md'.format(REPO))

# add README to github commit
os.system('git add README.md')

# display the status of git repo
os.system('git status')

# first commit of the local repo to synch it with the online created repo
os.system('git commit -m \"Type: New Repo | {}\"'.format(REPO_DESCRIPTION))

# origin string
origin_str = 'https://github.com/{}/{}.git'.format(USER,REPO)
# ssh rsa keys origin_str = 'git@github.com:{}/{}.git'.format(USER,REPO)

# add the remote location to synch the commit in the future
os.system('git remote add origin {}'.format(origin_str))

# push new repo to github of username using the master
os.system('git push -u origin master')

