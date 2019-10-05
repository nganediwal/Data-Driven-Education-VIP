This directory contains an example project that does a simple NLP-based analysis on the edX forum data.

Prerequisites:
* IRB Training
* Submit Qualtrics survey
    * download the repository
        * git clone https://github.gatech.edu/C21U/vip-nlp.git
        * https://github.gatech.edu/C21U/vip-nlp green button -> Download 
    * copy creds.zip to this directory
    * unzip creds.zip into this directory
    * make sure creds.py and .aws (this may be hidden on your filesystem) is in this directory
    * **NOTE: NEVER UPLOAD ANYTHING IN creds.zip TO GITHUB, .gitignore CONTAINS ALL ASSOCIATED FILES**
* Environment with python and packages installed
    * docker build -t nlp .
* Run docker image and enter a bash shell
    * docker run -it nlp
* Run program
    * python nlp_analysis.py
