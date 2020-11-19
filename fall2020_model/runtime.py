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


output_variable = "percent_progress"
filter_best_correlated = False

def read_csv(filepath, student_id):
    
    '''
    Return course data
    '''

    #Columns in events.csv - patient_id,event_id,event_description,timestamp,value
    data = pd.read_csv(filepath + 'course_data.csv')

    return data.iloc[[student_id]]

def clean_data_null(df):

    #drop English col
    df.drop(columns=['English'], inplace=True)


    #fill null in education and gender with unspecified
    df['level_of_education'].fillna('not specified', inplace=True)
    df['gender'].fillna('not specified', inplace=True)
    df['US'].fillna(-1, inplace=True)
    df['year_of_birth'].fillna(1987, inplace=True);
    return df;

	    

def main():
    data_path = './data/'
    student_id = 6550
    data=read_csv(data_path, student_id)
    data=clean_data_null(data)
    X_test = data.drop([output_variable], axis=1)
    y_test = data[output_variable]
    print('Original: ' + str(y_test[student_id]))
    loaded_model = joblib.load('./model/best_model.pkl')
    #result = loaded_model.score(X_test, Y_test)
    Ypredict = loaded_model.predict(X_test) 
    print('Predicted: ' + str(Ypredict[0]))
if __name__ == "__main__":
    main()