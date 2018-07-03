## Auto Repo (AR) App
--------------------------

**AR** is a web app developed on Flask, a light weight web micro framework.
It is a web app that interacts with the Github API to copy the app's containing repository from the app owner into a user's Github. 
The copied repository includes:

* Source code
* Necessary files for deployment
* Installation Manual
* Technical Specification

If you decide or decided to get **AR**, here we will teach you how to get it running on the web.

### Getting Started
--------------------------

The steps you will follow to deploy **AR** on the web are:

1. Deploy your **AutoRepo (AR)** repo into Heroku from your Github
2. Create an authorization OAuth in Github for your **AutoRepo (AR)** repo/app to be able to interact with Github API
3. Create a *configuration file* ```owner_info.txt``` that contains the Github OAuth credentials and commit it to your **AutoRepo (AR)** repo
4. Update the deployment in Heroku to take in the created ```owner_info.txt``` file and be able to run
5. Open your app in the browser and ENJOY!

These steps might seem intimidating, but we will guide you all the way until you deploy your **AR**.

### Deployment in Heroku
--------------------------
The first thing you need to do is login to your Heroku account. 

>**Note:** If you do not have an account, create a free account and log in. You can use the Heroku link below to go the *log in/sign up* page

Let's go to [Heroku](https://signup.heroku.com) to create a new app!

1. Log in to Heroku
2. Once logged into Heroku, you will see your dashboard (if you are new to Heroku, you will have no apps listed). 
3. Click the button that says **New** on the upper right corner of the page (your right)
4. Choose **Create new app**
5. Give a name to your app in the field **App name** (this is the name that will be shown in your URL)
6. Choose your current **Region/Country**
7. Once created the app, you will be redirected to a new website that describes your app settings, deployment, etc. We need to configure it.
8. In the Heroku app website, go to the **Settings** tab (if you don't see it you might have a logo of gears)
9. Scroll down until you find the word **Buildpacks** on the left side of the screen
10. Click on **Add buildpack** button on the right side of **Buildpacks** and select **Python**
11. Now, go to the **Deploy** tab (if you don't see it you might have a logo of of an arrow pointing upwards)
12. In the **Deploy** tab scroll down until you see **Deployment method** on the left side of the screen (your left)
13. In the **Deployment method** section click on the **Github** 
14. Then, just right below **Deployment method** select your Github account and the **AutoRepo** (or the repo that contains your AutoRepo (AR) app)
15. Click the button **Connect** 
16. A window from Github will pop up, **Authorize** the Heroku app to access your Github (You will not get the pop-up window if you have deployed an app through Heroku in the past)
17. Go to the **Manual Deploy** section and choose the **Master** branch
18. Click **Deploy**, you should see it has success

Now, you have deployed your app in Heroku. If you click the **View** button that appeared after successfully building your app, it will take you to your **home URL**. However, if someone tries to **Get the code!** of the app the way you got his one, your app will not work.

This is related to Github API authorization and also to the configuration file the app needs.

### Github API Authorization (OAuth App)
--------------------------

This next step is very important to allow our app to interact with the Github API. We will register an OAuth app in Github.

1. Go to your Github **Settings**, choose **Developer settings** and click the button **New OAuth App** or simply click this [link](https://github.com/settings/applications/new) to get there.
2. Choose a **name** for the app
3. From your deployment in Heroku you know your **home URL**, copy it into the form (Your home URL should be similar to: ```https://YOUR_APP_NAME.herokuapp.com```, where ```YOUR_APP_NAME``` is the name of your app in Heroku)
4. Give a description of your app
5. In **Authorization callback URL** you will need to trust me and type the following URL: ```https://YOUR_APP_NAME.herokuapp.com/done``` 
**Note: Make sure you replace ```YOUR_APP_NAME``` for the name of your app in Heroku**
6. Click **Register Application** that should register your app and redirect you to a website where you will see your application **Client ID** and **Client Secret**

We will need your **Client ID** and **Client Secret** to create the configuration file.


### AR Configuration File
--------------------------

The last item missing is to create the configuration file ```owner_info.txt``` and commit it to the repo that contains your AR app. **It is very important that you name this file ```owner_info.txt```**.

First, clone your repository on your local machine.
In that local repo create the file ```owner_info.txt```.

The configuration file content is as follow:

```json
{
    "owner": {
        "username": "YOUR_GITHUB_USERNAME",
        "repo": "YOUR_REPO_WITH_THE_AUTO_REPO_APP"
    },
    "user": {
        "repo": "REPO_NAME_TO_CREATE_ON_USER_GITHUB"
    },
    "app": {
        "client_id": "YOUR_CLIENT_ID_FROM_GITHUB_OAUTH_APP",
        "client_secret": "YOUR_CLIENT_SECRET_FROM_GITHUB_OAUTH_APP"
    }
}
```

You can copy the structure above and paste it in ```owner_info.txt```. Then, replace the strings:
1. ```YOUR_CLIENT_ID_FROM_GITHUB_OAUTH_APP``` with your **Client ID**
2. ```YOUR_CLIENT_SECRET_FROM_GITHUB_OAUTH_APP``` with your **Client Secret**
3. ```YOUR_GITHUB_USERNAME``` with your Github **username**
4. ```YOUR_REPO_WITH_THE_AUTO_REPO_APP``` with the name of your **repo** that contains the AutoRepo (AR) app
5. ```REPO_NAME_TO_CREATE_ON_USER_GITHUB``` with the name of the **repo** you will create on your user

Save the file again and commit it to your Github repo.
**Note: Stay on the *master* branch**
**Note:** The app doesn’t copy from the owner's repo the ```owner_info.txt``` file into the user’s repo as this file contains the owner's credentials (keep them safe)

### Update Deployment in Heroku
--------------------------

Finally, go back to Heroku and specifically to your app **Deploy** tab.
Once again, go down to **Manual Deploy** and click **Deploy Branch**

When it finishes deploying, you will get the **View** button, click it!

### CONGRATULATIONS!! 
--------------------------
#### Your app is alive!!




