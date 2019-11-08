# Contents
* creds.py - Python script containing credentials required to log in
* connect.py - helper Python script for connecting to mongo via pymongo. Will also start the ec2 instance if it's not currently running
* ec2_start.sh - Bash script that starts the ec2 instance if it's down
* mongo_connect.sh - connects to mongo database via the mongo command prompt
* .aws - hidden folder containing credentials to for aws access
* Dockerfile - example dockerfile that can be used to create a docker image which can run nlp_analysis.py
* requirements.txt - Python libraries required to run nlp_analysis.py
* nlp_analysis.py - runs a simple NLP analysis on data within the Mongo database

This repository contains the credentials needed to access the C21U mongo database. It also contains example scripts which connect to the database and run a simple NLP analysis along with bash scripts for connecting to the database via the Mongo command prompt.

# How to build docker image
* unzip c21u_mongo.zip
* make sure creds.py and .aws (this may be hidden on your filesystem) is in this directory
* **NOTE: NEVER UPLOAD ANYTHING IN creds.zip TO GITHUB, double check that creds.py and the Bash scripts are in .gitignore!!**
* Build the docker image
    * docker build -t nlp .
        * docker: the docker command line app
        * build: create a new image using a Dockerfile
        * -t nlp: name the new image nlp
        * .: use the Dockerfile in this directory

# How to use docker image
* Run docker image and enter a bash shell
    * docker run -it nlp
* Run program
    * python nlp_analysis.py
* Start ec2 instance
    * ./ec2_start.sh
* log into mongo shell
    * ./mongo_connect.sh
