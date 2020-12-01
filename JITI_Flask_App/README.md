# Just In Time Interventions Web App

This is the Web App for displaying the predition information and suggestions to students and teachers

# Installation Steps
* Install Anaconda following the guide in https://docs.anaconda.com/anaconda/install/
* Run anaconda
* Goto the folder .\vip-research\JITI_Flask_App\
* Run the below command

```
conda env create -f environment.yaml
```

* Once the enviornment is created run the below command to switch the environment 

```
conda activate VIP
```
* Then run python app.py to the application
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