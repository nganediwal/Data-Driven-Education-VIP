# Just In Time Interventions Web App

This is the Web App for displaying the predition information and suggestions to students and teachers

# Installation Steps
* Install Anaconda following the guide in https://docs.anaconda.com/anaconda/install/
* Run anaconda
* Goto the folder .\vip-research\JITI_Flask_App\
* Run the below command
```
conda env create -f requirements.yaml
```
* Once the enviornment is created run the below command to switch the environment 
```
conda activate VIP
```
* Then run python app.py to the application
* Open the web app using the url http://127.0.0.1:8050/


# Where to place ignored files
* "config.py" should have the credentials to accessing the C21U db and be placed in the same folder as app.py
* "course_data.csv" should have the data needed to predict course completion and should be stored in the folder "real_model"
