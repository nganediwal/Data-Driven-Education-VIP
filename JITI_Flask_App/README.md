# Just In Time Interventions Web App

This is the Web App for displaying the predition information and suggestions to students and teachers

# Installation Steps
## Install Anaconda and Create Environment
* Install Anaconda following the guide in https://docs.anaconda.com/anaconda/install/
* Run the anaconda install script
* cd to the folder vip-research\JITI_Flask_App\
* Run the command below to create a conda environment

```
conda env create -f env-min.yml
```

* Once the enviornment is created run the below command to switch the environment 

```
conda activate VIP
```
## Database Setup
The .gitignore file does not allow the config.py file to be uploaded to Github, so you are missing this file. 

You need to contact Dr. Lee for access to the database, after IRB training

## Config File Setup

Your config.py file should look like this:  
```python
# dummy config info
psql_db = 'your db'
psql_user = 'your user'
psql_host = 'your host'
psql_port = '5432'
psql_password = 'your password'
```
## Environment Variables Setup
At least on Linux, you need to run (if it's bash):  
`export FLASK_APP=app.py`  
`export FLASK_ENV=development`  

In Windows or Mac you'll have to look at your settings, I'm not sure if these are needed outside of Linux, so try without them set.

The FLASK_ENV=development means debugging is on and when you make changes to a file and save, the server will update with those changes.

## Running the App
* Then run python app.py to start the application
* Open the web app using the url http://127.0.0.1:8050/


# Where to place ignored files
* "config.py" should have the credentials to accessing the C21U db and be placed in the same directory as app.py
* "course_data.csv" should have the data needed to predict course completion and should be stored in the folder "real_model"

# Overview of App
The app is built using dash by plotly. This allows for powerful graphing features and easy integration with python ML libraries. See below for a general guide on where the various parts of the app are located.
* Modify Individual pages
    * "JITI_Flask_App/pages/"
    * home: "JITI_Flask_App/pages/index.py"
* Modify database connections / create new query functions
    * "JITI_Flask_App/studentdata.py
* Route modification
    * "JITI_Flask_App/app.py"
* Location of Completion percentage model (.pkl)
    * "JITI_Flask_App/real_model/"
* Location of Fake models (local)
    *  "JITI_Flask_App/temp_model/"

# Helpful Resources
* https://plotly.com/dash/