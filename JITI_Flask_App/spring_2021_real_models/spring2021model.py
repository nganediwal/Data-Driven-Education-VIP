import os
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.model_selection as model_selection
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

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
os.chdir("..") # directory is now whatever directory app.py is in

class Spring2021Models(object):

    def __init__(self):
        self.output_variable = "percent_grade"
        self.output_variable_agg = "percent_progress"
        self.filter_best_correlated = False

    def read_csv(self, filepath, student_id, course, week, timeseries):
        
        '''
        Return course data
        '''
        data = pd.read_csv(filepath + 'course_data_web_' + course + '.csv')
        #if timeseries:
        #    data=data[data['user_id']==student_id]
        #    return data[data['week']==week]
        #else:
        return data[data['user_id']==student_id]

    def clean_data_null(self, df, course):
        df = df.dropna()
        return df

    def removeBadColumns(self, df_in):
        del df_in['country']
        del df_in ["level_of_education"]
        del df_in ["gender"]
        df_in['age'] = pd.datetime.now().year - df_in.year_of_birth
        df_in['age'].fillna(df_in['age'].median(), inplace=True)
        del df_in ["year_of_birth"]
        return df_in

    def accumlate_data1(self, df):
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
        newdf=newdf.sort_values(['week']).reset_index(drop=True)
        for col in columns:
            newdf[col]=newdf.groupby(['user_id'])[col].cumsum(axis=0)  
        return newdf

    def clean_agg_data_null(self, df):
        #fill null in education and gender with unspecified
        df['level_of_education'].fillna('not specified', inplace=True)
        df['gender'].fillna('not specified', inplace=True)
        df['country'].fillna('not specified', inplace=True)
        return df;


    def clean_agg_data_outlier(self, df_in):
        df=df_in.copy()
        del df['country']
        df["level_of_education"]=df["level_of_education"].fillna("Not Specified")
        df = df.dropna(axis=0)
        del df ["level_of_education"]
        del df ["gender"]
        df['Age'] = pd.datetime.now().year - df.year_of_birth
        del df ["year_of_birth"]
        return df

    def run_agg_data(self, data, course):
        agg_data = data.groupby(
        ['user_id']
        ).agg(
            weeks_active=('week', 'count'),    # Sum duration per group
            gender= ('gender', 'first'),
            country=('country', 'first'),
            year_of_birth=('year_of_birth', 'first'),
            level_of_education=('level_of_education', 'first'),
            page_close_agg_count=('page_close', 'sum'),
            hypertext_agg_count=('hypertext', 'sum'),
            next_selected_agg_count=('next_selected', 'sum'),
            resume_course_agg_count=('resume_course', 'sum'),
            sidebar_agg_count=('sidebar', 'sum'),
            seq_goto_agg_count=('seq_goto', 'sum'),
            seq_next_agg_count=('seq_next', 'sum'),
            seq_prev_agg_count=('seq_prev', 'sum'),
            tool_accessed_agg_count=('tool_accessed', 'sum'),
            problem_check_agg_count=('problem_check', 'sum'),
            problem_graded_agg_count=('problem_graded', 'sum'),
            seek_video_agg_count=('seek_video', 'sum'),
            load_video_agg_count=('load_video', 'sum'),
            play_video_agg_count=('play_video', 'sum'),
            pause_video_agg_count=('pause_video', 'sum'),
            stop_video_agg_count=('stop_video', 'sum'),
            captions_hidden_agg_count=('captions_hidden', 'sum'),
            captions_shown_agg_count=('captions_shown', 'sum'),
            hide_transcript_agg_count=('hide_transcript', 'sum'),
            show_transcript_agg_count=('show_transcript', 'sum'),
            speed_change_video_agg_count=('speed_change_video', 'sum'),
            percent_progress=('percent_grade', 'first')
        )
        agg_data.reset_index(inplace=True)
        agg_data.drop(['user_id'], axis=1, inplace=True)
        agg_data=self.clean_agg_data_null(agg_data)
        agg_data=self.clean_agg_data_outlier(agg_data)
        print(agg_data.columns)
        X_test = agg_data.drop([self.output_variable_agg], axis=1)
        y_test = agg_data[self.output_variable_agg]
        # print('Original: ' + str(y_test))
        loaded_model = joblib.load('./spring_2021_real_models/' + course + '/best_model.pkl')
        #result = loaded_model.score(X_test, Y_test)
        Ypredict = loaded_model.predict(X_test) 
        return str(Ypredict[0])

    def run_timeseries_data(self, data, course, week):
        data = self.removeBadColumns(data)
        data = self.clean_data_null(data, course)
        data = self.accumlate_data1(data)
        data = data[data['week']==week]
        data.drop(columns=['user_id'], inplace=True)
        #print(data_timeseries.head())
        X_test = data.drop([self.output_variable], axis=1)
        y_test = data[self.output_variable]
        #print('Original: ' + str(y_test))
        loaded_model = joblib.load('./spring_2021_real_models/' + course + '/best_model_time_series.pkl')
        #result = loaded_model.score(X_test, Y_test)
        Ypredict = loaded_model.predict(X_test) 
        return str(Ypredict[0])

    def run_model(self, course, student_id, week=None):
        if course=='CS1301':
            data_path = './spring_2021_real_models/CS1301/'
        elif course=='MGT100':
            data_path = './spring_2021_real_models/MGT100/'
        timeseries = False
        if week != None:
            timeseries = True
        data=self.read_csv(data_path, student_id, course, week, timeseries)
        if timeseries:
            # print("Time Series")
            return self.run_timeseries_data(data, course, week)
        else:
            # print("Aggregated")
            return self.run_agg_data(data, course)

# def main():
#     #course = 'MGT100'
#     springmodel = Spring2021Models()
#     course = 'MGT100' 
#     student_id = 819642
#     #CS1301 id - 466451, week 12
#     #MGT100 id - 819642, week 12
#     week = None # give actual week for time series
#     print(springmodel.run_model(course, student_id, week))

# if __name__ == "__main__":
#     main()