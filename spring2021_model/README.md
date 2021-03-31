
# Just In Time Interventions Spring 2021 Data Model

This is the Model building project to predict percentage_complete from demographics and clickstream data

# Spring 2021 Deliverables

# Previous Work and Literature review
## Predicting Student Success
* [Gardner and Brooks, 2018: Model Evaluation Method](https://learning-analytics.info/journals/index.php/JLA/article/view/5814)
* [Davis et al., 2016: Student self-regulated success](https://angusglchen.github.io/documents/LAK16_Dan_Encouraging.pdf)
## edX Data Description
* [Davis et al., 2018: Design of edX MOOCs](https://dl.acm.org/citation.cfm?id=3231663)
## Interventions
* [Davis et al., 2018: Retrieval Practice](https://learning-analytics.info/journals/index.php/JLA/article/view/6098)
* [Kizilcec et al., 2017: Social Identity Threat ](http://science.sciencemag.org/content/sci/355/6322/251.full.pdf)

# Environmental Setup

To run the project below are the setup instructions.

* Install Anaconda following the guide in https://docs.anaconda.com/anaconda/install/
* Run anaconda
* Goto the folder .\vip-research\spring2021_model\
* Run the below command
```
conda env create -f environment.yml
```
* Once the enviornment is created run the below command to switch the environment 
```
conda activate vipspring2021
```
* Then run python model_pipeline.py build a model

# Input Data

Input data used for this research is an ammonized CSV file that contains data from a CS based MOOC course with demographics and clickstream.

* Input Variable


* Output Variable


# Approach

## Data Exploration


## Null data removal

All code related to null removal can be found in:
```
clean_data_null()
```

## Outlier data removal

All code related to outlier removal can be found in:
```
clean_data_outlier()
```

## Convert to Time Series

Change the clickstream data to a time series data:
Loop through the columns. If there are multiple 
users in a row then add to the total for that user.

All code related to converting the dataset to a timeseries can be found in:
```
accumulate_data()
```

## Feature Selection

All code related to Data exploration and feature selection can be found in:
```
feature_explortion()
```


## Model Training Pipeline and Hyperparamter tuning

All code related to training pipeline can be found in:
```
quick_eval() 
```

## Model Performance



## Results 


## Unsupervised Learning


