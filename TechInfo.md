## Auto Repo (AR) App - Overview
---------------------------------

**AR** is a web app developed on Flask. It interacts with the Github API to copy the app's containing repository from the app owner into a user's Github. As a result it is an [OAuth app](https://developer.github.com/apps/building-oauth-apps/) and  it follows a [web flow](https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/#web-application-flow) approach to authorize users for your app usage.

The way **AR** interacts with the Github API is through HTTP requests: 

* GET
* POST
* PATCH

It then parses the response to extract what it asked to Github API or to know if the request was successful. The Github API is a REST API and that is the main reason to use HTTP requests.

For more details on the Github API visit [Github Developer v3](https://developer.github.com/v3/). There is also a lean [getting started guide](https://developer.github.com/v3/guides/getting-started/) using ```curl``` that can be insightful.

Before you continue, please try to give a quick read to how Github system works as it will make it easier to understand the following section, visit [Git-Internals](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects).

### Flow of Repo Duplication
---------------------------------

The steps used in this app to duplicate a repository are:

1. Retrieve the owner’s repo SHA
2. Use the owner's repo SHA to retrieve the recursive tree structure that shapes the owner's repo
3. Request **public_only** access to the user’s Github profile and retrieve an **access_token** in the handshake of the authorization process
**Note:** Steps below need a user's access_token
4. Create a public repository in the user's Github
5. Use the tree structure retrieved from the owner's repo and modify it to create a valid tree to post in the user's repo.
    1. Remove the tree objects, url, size, truncated parameters. In other words, keep only blob objects except for the ```owner_info.txt``` file.
    2. Convert the cleaned tree in 'a' to a tree that instead of using the SHA of the blobs it uses each blob **content**. This is very important because it is the first time we add these files to the user's repo, so Github needs the content as it doesn't have any reference to any blob SHA. It is during this step that we create a blob for each file using its **content**, and we end up with a tree with blob content, but none blob SHA.
6. Use the tree with blob content to post it on the user's repo. If successful this step returns a SHA of the posted/created tree.
7. Use the posted/created tree SHA to create a commit. If successful it returns a SHA of the created commit.
8. Use the commit SHA to update the HEAD reference of the branch. In this case, we are using the master branch of the user.
9. After updating the reference the files will appear in the user's Github. If the HEAD reference is not updated all steps before 8 will not take any effect.

>**Note:** If you do not know what a SHA means for Github, we can say it is a *"40-character checksum hash of the content you’re storing plus a header"*

For another explanation on how to commit files from the Github API, visit [Levi Botelho's Coding Blog](http://www.levibotelho.com/development/commit-a-file-with-the-github-api/). He has a very clear explanation on this topic as well.

### Limitations
---------------------------------

There are some **limitations** to list that can be useful to know about our **AR** app.

1. Interaction with the **Github API** has a **maximum limit rate** of:
       
        * Authorized requests (OAuth apps with an access token) can ask for 5000 requests per hour per IP address.
        * Non-authorized requests cna ask only for 60 requests per hour per IP address.

    You can make authorized requests to the API if you use any fo the following in your HTTP request:
       
        * Access token in the header or as a parameter
        * Client ID and client secret as parameters
    
    Knowing this can help you understand if you are doing an authorized or non-authorized request. This can be very helpful if suddenly you get 403 error (Forbidden) from Github, which will mean you need to probably check if you have asked for more than 5000 or 60 request within an hour window period of time.
    There are other things you can do such as play with the Timezone if you must really need more than 5000 authorized requests per hour. However, the AR app does not support that right now.

    For more details on Github API maximum limit rate, visit [GithubAPI maximum rate-limit](https://developer.github.com/v3/#rate-limiting).

2. Currently, the app can only duplicate repositories with no media files. This implies that it doesn't support images, video, etc to be added as content in the Github tree object to be posted, commited and made HEAD reference.
AR only supports simple [Github blob objects](https://developer.github.com/v3/git/blobs/).

3. AR app is not going to create private repositories as it was configured to only ask for public_only scope. You can learn more about GithubAPI scopes for OAuth apps [here](https://developer.github.com/apps/building-oauth-apps/understanding-scopes-for-oauth-apps/).

4. AR app will duplicate the repo it is currently running on the Heroku platform.

If you find more limitations please add them and share them with the world!

Hope this all was helpful to you!




