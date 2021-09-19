# Just In Time Interventions Web App

This is the Web App for displaying the predition information and suggestions to students and teachers

# Installation Steps  

## Decide on your environment, recommend to use a Linux VM
* It's best if you run this in a VM because you'll install a lot of packages you normally wouldn't use
* When you're done with the class, you can just delete the VM and not have to uninstall a lot of stuff
* If you're using Windows or MacOS, it's up to you to know how to translate instructions to your env
* If you haven't already installed it, you can get VirtualBox or VMWare free, if you're on a Mac, use VMWare
* For a free VMWare license, [see the OIT page about VMWare](https://support.cc.gatech.edu/resources/downloads). Download [VirtualBox here](https://www.virtualbox.org/wiki/Downloads) 
* Then the recommendation is [Ubuntu 20.04, download the iso](https://ubuntu.com/download/desktop) and import the ova appliance into VirtualBox or VMWare 

There are still some things to tweak in the VM, such as Display and Network settings to get the VM working. Ask James for help.

If you want copy-paste to work between guest and host, you need to install Guest Additions in the VM and add the user to the vboxsf group.

Once you spin up your VM, open a terminal and follow the rest of the instructions below.

## Git instructions to clone the repo
* `cd` to your home directory or wherever you'd like to have a vip-research directory with the repo
* Run the following command:
```
git clone https://github.gatech.edu/C21U/vip-research.git
```
* NOTE: You may need to install git, run: `sudo apt install git`

## Install Anaconda and Create Environment
* Install Anaconda following the guide in https://docs.anaconda.com/anaconda/install/
* Run the anaconda install script
* Make sure you're in the vip-research folder, we're about to create a Conda environment, and it must be created here at the top level of the repo. 
* Run the command below to create a conda environment

```
conda env create -f JITI_Flask_App/env-min.yml
```

* Once the enviornment is created run the following commands to switch the environment 

```
conda activate VIP
```
* Now, cd to the JITI_Flask_App directory
```
cd JITI_Flask_App
```
## Installing VS Code in the VM
* If you chose the VM route, you probably want VS Code or Pycharm. 
* For VS Code, assuming you chose Ubuntu and have `snap` installed, run:
```
sudo snap install --classic code
```
* For PyCharm, because of libraries we use, you'll want the Pro version (needs a license through GA Tech), please run:
```
sudo snap install pycharm-professional --classic
```
* Then during the PyCharm launch, it will prompt you for a license key or Jetbrains login to activate the license.

## Database Setup
The .gitignore file does not allow the config.py file to be uploaded to Github, so you are missing this file. 

You need to contact Dr. Lee for access to the database, after IRB training

## Config File Setup

Your config.py file should look like this:  
```python
# dummy config info
psql_db =gatechmoocs
psql_user =<your username>
psql_host =gatechmoocs.cjlu8nfb8vh0.us-east-1.rds.amazonaws.com
psql_port = '5432'
psql_password =<your password>
```
## Environment Variables Setup
At least on Linux, you need to run (if it's bash):  
`export FLASK_APP=app.py`  
`export FLASK_ENV=development`  

It's best to set these in your ~/.bashrc file, so every login/terminal will have them set even after a reboot

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
* [Dash docs](https://dash.plotly.com/)
* [Datacamp DASH tutorial](https://www.datacamp.com/community/tutorials/learn-build-dash-python)