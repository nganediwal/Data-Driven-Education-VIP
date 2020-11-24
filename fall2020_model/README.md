# Just In Time Interventions Fall 2020 MOOC Data Model

This is the Model building project to predict percentage_complete from demographics and clickstream data

# Fall 2020 Deliverables
* Review modeling techniques from previous semeters
* Perform data Insights and generate plots
* Build automated pipeline for ETL and training
* Analyze feature importance
* Create a persisted model that can be queried online.

# Previous Work and Literature review
## Predicting Student Success
* [NEW Predicting student stop-out](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2611750)
* [Gardner and Brooks, 2018: Model Evaluation Method](https://learning-analytics.info/journals/index.php/JLA/article/view/5814)
* [Crossley et al., 2017: Cohesion Network Analysis](https://repository.isls.org/bitstream/1/220/1/17.pdf)
* [O'Connell
 et al., 2018: Long Term Prediction](https://learning-analytics.info/journals/index.php/JLA/article/view/5833)
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
* Goto the folder .\vip-research\fall2020_model\
* Run the below command
```
conda env create -f environment.yml
```
* Once the enviornment is created run the below command to switch the environment 
```
conda activate vipfall2020
```
* Then run python model_pipeline.py build a model

# Input Data

Input data used for this research is an ammonized CSV file that contains data from a CS based MOOC course with demographics and clickstream.

* Input Variable

** English
** gender
** year_of_birth
** level_of_education
** US
** Active_weeks
** page_close_agg_count
** hypertext_agg_count
** next_selected_agg_count
** resume_course_agg_count
** sidebar_agg_count
** seq_goto_agg_count
** seq_next_agg_count
** seq_prev_agg_count
** tool_accessed_agg_count
** problem_check_agg_count
** problem_graded_agg_count
** seek_video_agg_count
** load_video_agg_count
** play_video_agg_count
** pause_video_agg_count
** stop_video_agg_count
** captions_hidden_agg_count
** captions_shown_agg_count
** hide_transcript_agg_count
** show_transcript_agg_count
** speed_change_video_agg_count

* Output Variable

** percent_progress

# Approach 

## Null data removal

## Outlier data removal

## Feature Selection

## Model Training Pipeline and Hyperparamter tuning

## Model Performance

## Resutls 