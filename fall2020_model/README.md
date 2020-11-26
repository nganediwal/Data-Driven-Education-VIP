
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

Some interesting observations from the data:

-   65% Male
-   30% B degree
-   62% Non-US
-   Very low percentage completed more than 20% of the course

Some interesting plots from the data exploration process is shown below

![Percentage Progress distribution](https://github.gatech.edu/C21U/vip-research/blob/master/fall2020_model/plots/percent_progress.png)

![Gender distribution](https://github.gatech.edu/C21U/vip-research/blob/master/fall2020_model/plots/gender.png)

![Level of Education  distribution](https://github.gatech.edu/C21U/vip-research/blob/master/fall2020_model/plots/level_of_education.png)

![US distribution](https://github.gatech.edu/C21U/vip-research/blob/master/fall2020_model/plots/US.png)

## Null data removal

Null Removal was not part of the final ML pipeline and was handled separately by investigating various features and its relevant plot. Some of the approaches are listed below.

-   English - Had 93% null and hence was dropped.    
-   Gender, Level of Education and US - Null was preserved by replacing with  “u” (unspecified)
-   Year of Birth - Replaced null with median
    
For the analysis, box plots where used to see how replacing null values changed the distribution of the data. After the removal there was not much overall impact in the best feature. It was observed that US and year of Birth lowest 2 correlated.
All code related to null removal can be found in:
```
clean_data_null()
```

## Outlier data removal

Outlier Removal was not part of the final ML pipeline and was handled separately by investigating various features and its relevant plot. Some of the approaches are listed below.

-   The input to this step was the data after null removal.    
-   Box Plot to observe outliers
-   Create outlier table based on z-score
-   Remove absolute z-score >3

    
For the analysis, box plots where used to see how replacing null values changed the distribution of the data. After the removal there was not much overall impact in the best feature.
All code related to outlier removal can be found in:
```
clean_data_outlier()
```

## Feature Selection
For feature selection, the best correlated features with the  output variables was considered. Some of the observations are listed below.

-   Best features
	-   Problem Graded
	-   Problem Check
	-   Next Seq
	-   Video Load
	-   Stop Video
-   Problem Check and Problem Graded are highly correlated
-   Play Video and Pause Video are highly correlated.

All code related to Data exploration and feature selection can be found in:
```
feature_explortion()
```

Correlation heatmap is shown below

![Correlation Heat Map](https://github.gatech.edu/C21U/vip-research/blob/master/fall2020_model/plots/correlation.png)

## Model Training Pipeline and Hyperparamter tuning

The dataset was split to 75% train and 25% test set and then sklearn pipelineswas used to train the model. Using this approch we evaluated 7 different models. The pipeline included the following steps

-    15 best correlated fetures were seleted
-    Categorical variables were transformed using OneHotEncoder
-    Regression using Grid Search with hyper paramter tuning

Below are the 7 algorithms and its various hyper paramters that was used for model training and evaluation.

-    LinearRegression
	-   Hyper parameters: fit_intercept, normalize
-    Lasso
	-   Hyper parameters: alpha, fit_intercept, normalize
-    DecisionTreeRegressor
	-   Hyper parameters: max_depth, min_samples_leaf
-    RandomForestRegressor
	-   Hyper parameters: max_depth, min_samples_leaf
-    BaggingRegressor
	-   Hyper parameters: max_depth, min_samples_leaf, n_estimators
-    AdaBoostRegressor 
	-   Hyper parameters: max_depth, min_samples_leaf, n_estimators, loss, learning_rate
-    GradientBoostingRegressor
	-   Hyper parameters: max_depth, min_samples_leaf, n_estimators, learning_rate
-    KNNRegressor
	-   Hyper parameters: n_neighbors

All code related to training pipeline can be found in:
```
quick_eval() 
```

## Model Performance

Below are the performance results from the 7 algorithms and its various hyper paramters values that resulted in the best RMSE score.

-    LinearRegression
	-   Hyper parameters: fit_intercept=True, normalize=True
	-   Train RMSE: 0.033
-    Lasso
	-   Hyper parameters: alpha=.01, fit_intercept=True, normalize=False
	-   Train RMSE: 0.034
-    DecisionTreeRegressor
	-   Hyper parameters: max_depth=5, min_samples_leaf=8
	-   Train RMSE: 0.028
-    RandomForestRegressor
	-   Hyper parameters: max_depth=5, min_samples_leaf=14
	-   Train RMSE: 0.028
-    BaggingRegressor
	-   Hyper parameters: max_depth=4, min_samples_leaf=14, n_estimators=200
	-   Train RMSE: 0.029
-    AdaBoostRegressor 
	-   Hyper parameters: max_depth=4, min_samples_leaf=19, n_estimators=100, loss=exponencial, learning_rate=0.01
	-   Train RMSE: 0.029
-    GradientBoostingRegressor
	-   Hyper parameters: max_depth=5, min_samples_leaf=1, n_estimators=300, learning_rate=0.1
	-   Train RMSE: 0.018
-    KNNRegressor
	-   Hyper parameters: n_neighbors=11
	-   Train RMSE: 0.027

RMSE on the train and test data is shown in the below plot

![Model Performance](https://github.gatech.edu/C21U/vip-research/blob/master/fall2020_model/plots/model_plots/algorithms.png)

## Resutls 

Our project replicated much of the work from Garner & Brooks. We applied the predictive modeling techniques mentioned in the paper to find the best predictive model for the problem. Garner & Brooks found that using clickstream data and non-parametric tree-based models produced the most accurate predictions. Our findings align with this claim, with our best model being Gradient Boosting Regressor

Below is the summary of results:

-   Gradient Boosted trees worked best.
-   All others trees were close.
-   Linear Algorithms did not perform well.
-   Final RMSE: 0.018
-   The final model performed great for lower % progress values but did not perform well for higher % progress, indicating some bias in the model.

## Unsupervised Learning

As a part of verifying the featture important and getting an insight of how data is seperated, unsupervised learning was caried out with the data. Below are some highlights.

-   Ran multiple clustering algorithms, 
-   Selected Cosine k Means using Silhouette Score as the factor
-   Found 3 clusters to be the best using elbow method

Below plot shows the main features that contributed for seperating the data into 3 clusters.

![Clusters & Features](https://github.gatech.edu/C21U/vip-research/blob/master/fall2020_model/plots/clustering_results.png)




