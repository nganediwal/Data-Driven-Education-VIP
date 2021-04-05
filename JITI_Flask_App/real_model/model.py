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
os.chdir("..")

class GradePredModel(object):
    def __init__(self):
        self.output_variable = "percent_progress"
        self.filter_best_correlated = False

    def read_csv(self, filepath=None, student_id=None):
        if(filepath == None):
            data = pd.read_csv('course_data.csv')
        else:
            data = pd.read_csv(filepath + 'course_data.csv')
        temp = data.iloc[[student_id]]
        return temp

    def clean_data_null(self, df):
        #drop English col
        df.drop(columns=['English'], inplace=True)

        #fill null in education and gender with unspecified
        df['level_of_education'].fillna('not specified', inplace=True)
        df['gender'].fillna('not specified', inplace=True)
        df['US'].fillna(-1, inplace=True)
        df['year_of_birth'].fillna(1987, inplace=True)
        return df

    # student_id = 44987
    def predict_completion(self, student_id):
        data_path = './real_model/'
        data=self.read_csv(data_path, student_id=student_id)
        data=self.clean_data_null(data)
        X_test = data.drop([self.output_variable], axis=1)
        loaded_model = joblib.load('./real_model/best_model.pkl')
        Ypredict = loaded_model.predict(X_test)
        return Ypredict[0]