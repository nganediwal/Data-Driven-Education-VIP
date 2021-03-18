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


output_variable = "percent_progress"
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
    if course == 'CS1301':
        df = df.dropna()
    return df;

def clean_data_outlier(df_in):
   return df_in

def transform_data(df_in):
	# Add each Event Type as a columns.
    df_in["event_type"].replace({"edx.bi.course.upgrade.sidebarupsell.displayed": "sidebar", "edx.ui.lms.link_clicked": "hypertext", "edx.course.tool.accessed": "tool_accessed","edx.video.closed_captions.hidden": "captions_hidden", "edx.video.closed_captions.shown": "captions_shown", "edx.ui.lms.sequence.next_selected": "next_selected", "edx.course.home.resume_course.clicked": "resume_course"}, inplace=True)
    new_data = df_in.pivot_table('count', ['course_id', 'user_id','week'], 'event_type')
    new_data.reset_index( drop=False, inplace=True )
    return new_data

def main():
    writecsv = False
    course = 'MGT100'
    #course = 'CS1301'
    data_path = './data/'
    data, demog, output =read_csv(data_path, course)
	#write csv data to file for debugging using excel filters
    if writecsv:
        write_csv(data_path, data, course)
    print("Data Shape With Nulls: ", data.shape)
    data = clean_data_null(data, course)
    print("Data Shape without Nulls: ", data.shape)
    #clean_data_outlier(data)
    #print(data.event_type.unique())
    data = transform_data(data)
    data = data.replace(np.nan,0)
    data = pd.merge(data, demog, on="user_id")
    data = pd.merge(data, output, on="user_id")
    data.drop(columns=['course_id'], inplace=True) 
    data = accumlate_data(data)
    print(data.head())
    #model_pipeline_agg.runAnalysisForAggregatedData(data, course)


if __name__ == "__main__":
    main()
