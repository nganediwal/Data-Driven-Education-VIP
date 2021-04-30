
# Just In Time Interventions Spring 2021 Data Model

This is the Model building project to predict percentage_complete from demographics and clickstream data

# Spring 2021 Deliverables

* Review modeling techniques from previous semeters and extend it for MGT Course
* Perform data Insights and generate plots for MGT Course and compare it with CS Course
* Build automated pipeline for ETL and training for aggregated model for both CS and MGT Course and compare.
* Build automated pipeline for ETL and training for time series model for both CS and MGT Course and compare.
* Create a persisted model that can be queried online for all the course and both aggregated and time-series


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

	* English
	* gender
	* year_of_birth
	* level_of_education
	* US
	* Active_weeks
	* page_close_agg_count
	* hypertext_agg_count
	* next_selected_agg_count
	* resume_course_agg_count
	* sidebar_agg_count
	* seq_goto_agg_count
	* seq_next_agg_count
	* seq_prev_agg_count
	* tool_accessed_agg_count
	* problem_check_agg_count
	* problem_graded_agg_count
	* seek_video_agg_count
	* load_video_agg_count
	* play_video_agg_count
	* pause_video_agg_count
	* stop_video_agg_count
	* captions_hidden_agg_count
	* captions_shown_agg_count
	* hide_transcript_agg_count
	* show_transcript_agg_count
	* speed_change_video_agg_count

* Output Variable

	* percent_progress

# Approach

## Data Exploration
- Used various data visualization techniques such as scatter plots, 
- Correlation matrix, and other descriptive statistics to identify patterns and understand data better.

## Null data removal

### MGMT100 Course Data
- There were 127 records that had missing user_id. 
- MNAR →  Replaced all the records with missing user_id with specific user_id. 
### CS1301 Course Data
- There were 10322 records that had missing user_id. 
- MCAR →  Removed missing records with missing user_id 

All code related to null removal can be found in:
```
clean_data_null()
```

## Outlier data removal
- Visualized outliers using Box Plots & Histograms
- Obtained context on existence of outliers to determine handling decision
- Evaluated the removal of outliers using IQR and Z-score
- Found Z-score to retain most data and keep context so implemented z-score as final outlier removal method. 

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

The dataset was split to 75% train and 25% test set using GroupShuffleSplit and then sklearn pipeline was used to train the model. Using this approch we evaluated 7 different models. The hyperparemater is set with a if condition based on the course anme.

All code related to training pipeline can be found in:
```
quick_eval() 
```

## Imbalanced Data Removal

Imabalaced data was fixed using  SMOTE for Regression using the library SMOGN (https://pypi.org/project/smogn/). Below code was used to do the analysis but was commented for the final model evaluation for performance reasons.
```
train_data_by_user = smogn.smoter(data=train_data_by_user.reset_index(drop=True), y = "percent_grade")
```

	- Troubleshooting
	Using the above code gives a error in the code that canbe removed by following the instructions in the link(https://github.com/nickkunz/smogn/issues/12)


## Aggregated Supervised Learning

The aggregated alanylsis is impleted in the file model_pipeline_agg.py with the same methods developed in Fall2020

## Plots and charts

All plots and charts can be found  in the folder https://github.gatech.edu/C21U/vip-research/blob/master/spring2021_model/plots/model_plots/

