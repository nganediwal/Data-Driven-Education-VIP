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

def accumlate_data(df):
    ''' Change the clickstream data to a time series data:
        Loop through the columns. If there are multiple 
        users in a row then add to the total for that user'''
    newdf = df.copy()

    columns = ['captions_hidden', 'captions_shown',
       'hide_transcript', 'hypertext', 'load_video', 'next_selected',
       'page_close', 'pause_video', 'play_video', 'problem_check',
       'problem_graded', 'resume_course', 'seek_video', 'seq_goto', 'seq_next',
       'seq_prev', 'show_transcript', 'sidebar', 'speed_change_video',
       'stop_video', 'tool_accessed']
    
    for col in columns:
        lastuser = newdf['user_id'][0]
        total = 0
        i = 0
        while i < newdf['user_id'].count():
            if (newdf['user_id'][i] == lastuser):
                total = total + newdf[col][i]
                #print('match!', i, 'total',total)
                newdf[col][i] = total
            else:
                total = 0
                #print('new user found')
                lastuser = newdf['user_id'][i]
            i = i+1
    return newdf

def clean_data_null(df, course):
    # added course parameter to differentiate cleanup method
    if course == 'MGT100':
        df["user_id"].fillna(2402236, inplace = True)
        df = df.dropna()
    if course == 'CS1301':
        df = df.dropna()
    return df;

def clean_data_outlier(df_in):
   del df_in['country']
   df_in['Age'] = pd.datetime.now().year - df_in.year_of_birth
   del df_in ["year_of_birth"]
   return df_in

def transform_data(df_in):
	# Add each Event Type as a columns.
    df_in["event_type"].replace({"edx.bi.course.upgrade.sidebarupsell.displayed": "sidebar", "edx.ui.lms.link_clicked": "hypertext", "edx.course.tool.accessed": "tool_accessed","edx.video.closed_captions.hidden": "captions_hidden", "edx.video.closed_captions.shown": "captions_shown", "edx.ui.lms.sequence.next_selected": "next_selected", "edx.course.home.resume_course.clicked": "resume_course"}, inplace=True)
    new_data = df_in.pivot_table('count', ['course_id', 'user_id','week'], 'event_type', aggfunc='first')
    new_data.reset_index( drop=False, inplace=True )
    return new_data

def main():
    writecsv = True
    run_aggregated_analysis = False
    #course = 'MGT100'
    course = 'CS1301'
    data_path = './data/'
    data, demog, output =read_csv(data_path, course)
    print("Data Shape With Nulls: ", data.shape)
	#write csv data to file for debugging using excel filters
    if writecsv:
        write_csv(data_path, data, course)
    print("Data Shape without Nulls: ", data.shape)
    #clean_data_outlier(data)
    #print(data.event_type.unique())
    data = transform_data(data)
    data = data.replace(np.nan,0)
    data = pd.merge(data, demog, on="user_id")
    data = pd.merge(data, output, on="user_id")
    data.drop(columns=['course_id'], inplace=True) 
    if run_aggregated_analysis:
        print("Running Aggregated analysis..............")
        model_pipeline_agg.runAnalysisForAggregatedData(data, course)
    print("Running Cumalitive sum by week..............")
    data_timeseries = accumlate_data(data)
    data_timeseries = clean_data_null(data_timeseries, course)
    data_timeseries = clean_data_outlier(data_timeseries)
    print(data_timeseries.head())
    print("Running Time Series analysis..............")
    #xVars = feature_explortion_agg(agg_data, course)
    X = data_timeseries.drop([output_variable], axis=1)
    y = data_timeseries[output_variable]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.90,test_size=0.10, random_state=2020)
    train_data = X_train.copy()
    train_data[output_variable] = y_train
    #if(filter_best_correlated):
	#    preprocessor = preprocessor_best_features_agg(xVars)
    #else:
    preprocessor = preprocessor_categorical()
    print("Running Time Series Model analysis..............")
    regressors = [
        {
            'estimator':KNeighborsRegressor(),  
            'params':{'regressor__n_neighbors':np.arange(10, 15)}
        },
		{
            'estimator':GradientBoostingRegressor(), 
            'params':{
                'regressor__max_depth':np.arange(5, 6), 
                'regressor__min_samples_leaf':np.arange(1, 2)
            }
		}
    ]
    rows = []
    max_score=100;
    for r in regressors:
        pipe = Pipeline(steps = [
           ('preprocessor', preprocessor),
           ('regressor', r['estimator'])
        ])
        best_model, train_score, test_score = quick_eval(pipe, X_train, y_train, X_test, y_test, r['params'])
        #if(filter_best_correlated):
        #    plot_best_features(best_model, xVars, course)
        if(train_score<max_score):
            max_score=train_score
            final_model=best_model    
        rows.append([r['estimator'].__class__.__name__, train_score, test_score])
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
