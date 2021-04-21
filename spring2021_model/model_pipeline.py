import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.model_selection as model_selection
from sklearn.feature_selection import SelectKBest,f_regression
from sklearn import preprocessing
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Lasso, Ridge, LassoLars
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor, BaggingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import MinMaxScaler
from collections import Counter, OrderedDict
from ast import literal_eval
from itertools import chain
import matplotlib.pyplot as plt
from pandas import read_excel
from scipy import stats
from sklearn.externals import joblib
import model_pipeline_agg
#import smogn

output_variable = "percent_grade"
filter_best_correlated = True

def read_csv(filepath, course):

    '''
    Return course data
    '''
    data = pd.read_csv(filepath + 'course_data_' + course + '.csv')
    for col in data.columns:
        if 'Unnamed' in col:
            data.drop([col], axis=1, inplace=True)
    column_names = ['course_id', 'user_id', 'week', 'event_type', 'count']
    df = pd.DataFrame(columns = column_names)
    for i in range(0, len(data.columns), 5):
        df2 = pd.DataFrame(data.iloc[:, i:i+5].dropna(thresh=4))
        df2.columns=column_names
        df = df.append(df2, ignore_index=True)
    print(df.columns)
    #Output Data
    output_data = pd.read_csv(filepath + 'output_data_' + course + '.csv')
    output_data.drop(columns=['course_id'], inplace=True)
    #Demographics
    demog_data = pd.read_csv(filepath + 'demographics_data_' + course + '.csv')
    demog_data.drop(columns=['course_id'], inplace=True)
    return (df,demog_data,output_data)

def write_csv(filepath, data, course):

    '''
    Write course data in csv for debugging purposes
    '''
    data.to_csv(filepath + 'course_data_transformed_' + course + '.csv', index=False)

def write_csv_for_web(filepath, data, course):

    '''
    Write course data in csv for debugging purposes
    '''
    data.to_csv(filepath + 'course_data_web_' + course + '.csv', index=False)

def accumlate_data(df):
    ''' Change the clickstream data to a time series data:
        Loop through the columns. If there are multiple
        users in a row then add to the total for that user'''

    columns = ['captions_hidden', 'captions_shown',
       'hide_transcript', 'hypertext', 'load_video', 'next_selected',
       'page_close', 'pause_video', 'play_video', 'problem_check',
       'problem_graded', 'resume_course', 'seek_video', 'seq_goto', 'seq_next',
       'seq_prev', 'show_transcript', 'sidebar', 'speed_change_video',
       'stop_video', 'tool_accessed']
    df=df.sort_values(['week']).reset_index(drop=True)
    for col in columns:
        df[col]=df.groupby(['user_id'])[col].cumsum(axis=0)
      
    return df

def clean_data_null(df, course):
    # added course parameter to differentiate cleanup method
    if course == 'MGT100':
        df["user_id"].fillna(2402236, inplace = True)
        df = df.dropna()
    if course == 'CS1301':
        df = df.dropna()
    return df;

def visualize_raw_data_outlier(df_in, course):
    # Visualize outliers using boxplot
    df_in.boxplot(column=['count'], by='event_type', fontsize= 5)
    plt.savefig('./plots/' + course+ '/box_plot_by_event_type.png')

    # Visualize outliers using histograms
    df_in['count'].hist(by= df_in['event_type'])
    plt.savefig('./plots/' + course+ '/histogram_by_event_type.png')

def removeBadColumns(df_in):
    del df_in['country']
    del df_in ["level_of_education"]
    del df_in ["gender"]
    df_in['age'] = pd.datetime.now().year - df_in.year_of_birth
    df_in['age'].fillna(df_in['age'].median(), inplace=True)
    del df_in ["year_of_birth"]
    return df_in

def clean_data_outlier(df_in):
    # Visualize outliers using boxplot
    #df_in.boxplot(column=['count'], by='event_type', fontsize= 5)
    #plt.show()

    # Visualize outliers using histograms
    #df_in['count'].hist(by= df_in['event_type'])
    #plt.show()
    #print("Grouping")
    #df_grouped = df_in.groupby(['event_type'])['count']
    # Remove outliers using Z-score
    #df_in = df_in.dropna(axis=0)
    abs_z_scores = np.abs(stats.zscore(df_in))
    
    # Use threshold of 3 for sd
    print("Finding index by zscores")
    filtered_entries = (abs_z_scores < 4).all(axis=1)
    print("Filtering by zscores")
    df_out = df_in[filtered_entries]
    # print(df_out)

    return df_out;

def transform_data(df_in):
	# Add each Event Type as a columns.
    df_in["event_type"].replace({"edx.bi.course.upgrade.sidebarupsell.displayed": "sidebar", "edx.ui.lms.link_clicked": "hypertext", "edx.course.tool.accessed": "tool_accessed","edx.video.closed_captions.hidden": "captions_hidden", "edx.video.closed_captions.shown": "captions_shown", "edx.ui.lms.sequence.next_selected": "next_selected", "edx.course.home.resume_course.clicked": "resume_course"}, inplace=True)
    new_data = df_in.pivot_table('count', ['course_id', 'user_id','week'], 'event_type', aggfunc='first')
    new_data.reset_index( drop=False, inplace=True )
    return new_data

def main():
    writecsv = False
    writecsv_for_web = True
    run_aggregated_analysis = False
    #course = 'MGT100'
    course = 'CS1301'
    data_path = './data/'
    data, demog, output =read_csv(data_path, course)
	#write csv data to file for debugging using excel filters
    if writecsv:
        write_csv(data_path, data, course)
	#Commenting the below visualizations as it takes very long to generate the plots.
    #visualize_raw_data_outlier(data, course)
    data = transform_data(data)
    print("Data Transformation Completed...")
    data = data.replace(np.nan,0)
    data = pd.merge(data, demog, on="user_id")
    data = pd.merge(data, output, on="user_id")
    data.drop(columns=['course_id'], inplace=True)
    if run_aggregated_analysis:
        print("Running Aggregated analysis..............")
        model_pipeline_agg.runAnalysisForAggregatedData(data, course)
    if writecsv_for_web:
        write_csv_for_web(data_path, data, course)
    data = removeBadColumns(data)
    print("Data Shape With Nulls: ", data.shape)
    data = clean_data_null(data, course)
    print("Data Shape without Nulls: ", data.shape)
    #data = clean_data_outlier(data)
    print("Data Shape Without Outliers: ", data.shape)
    print("Running Cumalitive sum by week..............")
    data_timeseries = accumlate_data(data)
    print("Running Time Series analysis..............")
    #xVars = feature_explortion_agg(agg_data, course)
	# splitting data based on user id groups so that data from one user does not get split into test set and train set.
    train_inds, test_inds = next(model_selection.GroupShuffleSplit(test_size=.20, n_splits=2, random_state = 2020).split(data_timeseries, groups=data_timeseries['user_id']))
    data_timeseries.drop(columns=['user_id'], inplace=True)
    train_data_by_user = data_timeseries.iloc[train_inds]
    #print("Adding synthetic data..", train_data_by_user.shape)
    #train_data_by_user = smogn.smoter(data=train_data_by_user.reset_index(drop=True), y = "percent_grade")
    #print("Completed synthetic data..", train_data_by_user.shape)
    test_data_by_user = data_timeseries.iloc[test_inds]
    X_train = train_data_by_user.drop([output_variable], axis=1)
    y_train = train_data_by_user[output_variable]
    X_test = test_data_by_user.drop([output_variable], axis=1)
    y_test = test_data_by_user[output_variable]
    train_data = X_train.copy()
    train_data[output_variable] = y_train
	# preprocessor to convert stirng variables to categorical
    #preprocessor = preprocessor_categorical()
    print("Running Time Series Model analysis..............")
    regressors = [
        {
            'estimator':KNeighborsRegressor(),
            'params':{'regressor__n_neighbors':np.arange(10, 12)}
        },
		{
            'estimator':GradientBoostingRegressor(),
            'params':{
                'regressor__max_depth':np.arange(8, 10),
                'regressor__min_samples_leaf':np.arange(10, 15),
            }
		}
    ]
    rows = []
    max_score=100;
	#loop over each regressor and evaluate train errors.
    for r in regressors:
        pipe = Pipeline(steps = [
           #('preprocessor', preprocessor),
           ('regressor', r['estimator'])
        ])
        best_model, train_score, test_score = quick_eval(pipe, X_train, y_train, X_test, y_test, r['params'])
        #if(filter_best_correlated):
        #    plot_best_features(best_model, xVars, course)
        if(train_score<max_score):
            max_score=train_score
            final_model=best_model
        rows.append([r['estimator'].__class__.__name__, train_score, test_score])
    max_wk = test_data_by_user["week"].max()
    print("Max Wk",max_wk)
    wk_rows = []
    for wk in np.arange(1.0,max_wk,2.0):
        df_filterd = test_data_by_user[test_data_by_user['week']==wk]
        X_test = df_filterd.drop([output_variable], axis=1)
        y_test = df_filterd[output_variable]
        if len(X_test.index) == 0:
            continue
        y_test_pred = final_model.predict(X_test)
        test_score = np.sqrt(mean_squared_error(y_test, y_test_pred))
        wk_rows.append([wk, test_score])
    data_requirement = pd.DataFrame(wk_rows, columns=["week", "score"])
    data_requirement = data_requirement.set_index("week")
    print(data_requirement)
    fig = data_requirement.plot(kind='line').get_figure()
    fig.savefig('./plots/' +course + '/model_plots/data_requirement_by_week.png') 
	#Persist the model for use by Web.
    joblib.dump(final_model, './model/' + course + '/best_model_time_series.pkl')
    output = pd.DataFrame(rows, columns=["Algorithm", "Train RMSE", "Test RMSE"])
    output = output.set_index("Algorithm")
    print(output)
    fig = output.plot(kind='barh').get_figure()
    fig.savefig('./plots/' +course + '/model_plots/algorithms_time_series.png',bbox_inches='tight')

def preprocessor_categorical():
    categorical = ColumnTransformer(
    [
        ("categorical",  OneHotEncoder(dtype=np.int),['gender','level_of_education']),
    ],
    remainder="passthrough",
    )
    return categorical

def quick_eval(pipeline, X_train, y_train, X_test, y_test, params, verbose=True):
    """
    Trains modeling pipeline using Grid Search on hyper parameters passed and evaluates on train data.      Returns the best model, training RMSE, and testing
    RMSE as a tuple.
    """
    CV = GridSearchCV(pipeline, params, scoring = 'neg_mean_absolute_error', n_jobs= 6, cv=10)
    CV.fit(X_train, y_train)
    y_train_pred=CV.predict(X_train)
    y_test_pred=CV.predict(X_test)
    print(CV.best_params_)
    train_score = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_score = np.sqrt(mean_squared_error(y_test, y_test_pred))

    if verbose:
        print(f"Regression algorithm: {pipeline.named_steps['regressor'].__class__.__name__}")
        print(f"Train RMSE: {train_score}")
        print(f"Test RMSE: {test_score}")

    return CV.best_estimator_, train_score, test_score

def plot_best_features(estimator, xVars, course):
    #if the estimator has an option to provide best features, plot it
    if(hasattr(estimator.named_steps['regressor'], 'feature_importances_')):
        plt.figure(figsize=(25,25))
        plt.clf()
        plt.ylabel('Feature Importance Score')
        importances = estimator.named_steps['regressor'].feature_importances_
        feature_size=importances.shape[0]
        indices = np.argsort(importances)[::-1]
        plt.figure()
        plt.title("Feature importances - " + estimator.named_steps['regressor'].__class__.__name__)
        plt.margins(0.1)
        plt.bar(range(feature_size), importances[indices],align="center")
        plt.xticks(range(feature_size), np.array(xVars)[indices], rotation=45, ha='right')
        plt.xlim([-1, feature_size])
        plt.subplots_adjust(left=0.2, bottom=0.37)
        plt.savefig('./plots/' + course+ '/model_plots/' +estimator.named_steps['regressor'].__class__.__name__ + '_time_series.png')

if __name__ == "__main__":
    main()
