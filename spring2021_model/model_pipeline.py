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
    return df

def write_csv(filepath, data, course):
    
    '''
    Write course data in csv for debugging purposes
    '''
    data.to_csv(filepath + 'course_data_transformed_' + course + '.csv', index=False)

def clean_data_null(df):
    return df.dropna();
    

def clean_data_outlier(df_in):
   return df_in


def main():
    writecsv = False
    course = 'MGT100'
    #course = 'CS1301'
    data_path = './data/'
    data=read_csv(data_path, course)
    if writecsv:
        write_csv(data_path, data, course)
    print("Data Shape With Nulls: ", data.shape)
    #data = clean_data_null(data)
    print("Data Shape without Nulls: ", data.shape)
    #clean_data_outlier(data)
    
if __name__ == "__main__":
    main()