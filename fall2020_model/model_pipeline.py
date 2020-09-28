import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.model_selection as model_selection
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Lasso, Ridge, LassoLars
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from collections import Counter, OrderedDict
from ast import literal_eval
from itertools import chain

output_variable = "percent_progress"

def read_csv(filepath):
    
    '''
    Return course data
    '''

    #Columns in events.csv - patient_id,event_id,event_description,timestamp,value
    data = pd.read_csv(filepath + 'course_data.csv')

    return data


def quick_eval(pipeline, X_train, y_train, X_test, y_test, verbose=True):
    """
    Quickly trains modeling pipeline and evaluates on test data.      Returns original model, training RMSE, and testing
    RMSE as a tuple.
    """
    
    pipeline.fit(X_train, y_train)
    y_train_pred = pipeline.predict(X_train)
    y_test_pred = pipeline.predict(X_test)
    
    train_score = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_score = np.sqrt(mean_squared_error(y_test, y_test_pred))
    
    if verbose:
        print(f"Regression algorithm: {pipeline.named_steps['regressor'].__class__.__name__}")
        print(f"Train RMSE: {train_score}")
        print(f"Test RMSE: {test_score}")
    
    return pipeline.named_steps['regressor'], train_score, test_score

def feature_explortion(data):
    '''
    Explore features and return a list of features thats needs to be included in the model
    '''
    print("Data size: " + str(data.shape))
    print(data.isnull().sum().sort_values(ascending=False))
    corr_matrix = data.corr()
    cm=corr_matrix[output_variable].sort_values(ascending=False)
    features = cm.index[1:6].tolist()
    data[np.array(features)].hist(bins=200,figsize=(16,8))
    plt.savefig('./plots/Figure 1.png') 
    return features

def preprocessor_pipe(features):
    '''
    Create a pipeline for preprocessing data
    '''
    arr = np.array(features)
    print(arr)
    preprocessor = ColumnTransformer(
    [
        ("select", "passthrough",
            arr),
    ],
    remainder="drop",
    )
    return preprocessor

def main():
    data_path = './data/'
    data=read_csv(data_path)
    X = data.drop([output_variable], axis=1)
    y = data[output_variable]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.65,test_size=0.35, random_state=2020)
    train_data = X_train.copy()
    train_data[output_variable] = y_train
    xVars = feature_explortion(train_data)
    preprocessor = preprocessor_pipe(xVars)
    pca = PCA()
    regressors = [
        LinearRegression(),
        Lasso(alpha=.5),
        Ridge(alpha=.1),
        LassoLars(alpha=.1),
        DecisionTreeRegressor(),
        RandomForestRegressor(),
        AdaBoostRegressor(),
        GradientBoostingRegressor()
    ]

    for r in regressors:
        pipe = Pipeline(steps = [
           ('preprocessor', preprocessor),
           ('regressor', r)
        ])
        quick_eval(pipe, X_train, y_train, X_test, y_test)

if __name__ == "__main__":
    main()