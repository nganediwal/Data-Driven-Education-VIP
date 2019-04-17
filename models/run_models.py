import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import scipy
import numpy as np
import pprint
import sys
import itertools
import graphviz 
from dateutil import parser
from sklearn import preprocessing
from sklearn import model_selection
from sklearn import tree
from sklearn.pipeline import make_pipeline, make_union
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier as RF 
from sklearn.ensemble import AdaBoostClassifier as ABC
from sklearn.ensemble import GradientBoostingClassifier as GBC
from sklearn.linear_model import LogisticRegression as LR
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score as auc
from sklearn.metrics import roc_curve

# Constants

seeds = [141, 3251, 145, 16, 415, 7648, 534, 789, 3297, 135]
n_folds = 2
seeds = seeds[:5]

# grade_map = {0:0, 1:0, 2:0, 3:1, 4:1}

grade_cutoff = 0.81

# Feature vectors grouped into categories


imp_mean = preprocessing.Imputer(missing_values=np.nan, strategy='mean')
scaler = preprocessing.RobustScaler()

# A library of models. You may want to leave out MLPClassifier since it is neural-network based and requires significant compute
estimators = [
    {
        'name': 'random_forest',
        'value': RF(random_state=0),
        'parameters':
        {
            'imputer__strategy': ['mean', 'median'],
            'randomforestclassifier__n_estimators': [5, 10, 100],
            'randomforestclassifier__criterion' : ['gini', 'entropy'],
            'randomforestclassifier__max_features': ['auto', 'sqrt', 'log2']
        }
    },
    {
        'name': 'gradient_boost',
        'value': GBC(random_state=0),
        'parameters': 
        {
            'gradientboostingclassifier__n_estimators': [5, 10, 100],
            'gradientboostingclassifier__learning_rate': [1e-2, 1e-1, 1, 1e1],
            'gradientboostingclassifier__loss': ['deviance', 'exponential']
        }
    }, 
    {
        'name': 'logistic_regression',
        'value': LR(random_state=0),
        'parameters': 
        {
            'logisticregression__penalty': ['l1', 'l2'],
            'logisticregression__C': [0.01, 0.1, 1, 10, 100]
        }
    },
    {
        'name': 'SVM',
        'value': SVC(),
        'parameters':
        {
            'svc__kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'svc__C': [0.01, 0.1, 1, 10, 100]
        }
    },
    # },
    # {
    #     'name': 'MLPClassifier',
    #     'value': MLPClassifier(),
    #     'parameters':
    #     {
    #         'mlpclassifier__hidden_layer_sizes': [2, 5, 10],
    #         'mlpclassifier__alpha': [0.0001, 0.001, 0.01],
    #         'mlpclassifier__activation': ['relu', 'logistic']
    #     }
    # },
    {
        'name': 'ADABoost',
        'value': ABC(),
        'parameters':
        {
            'adaboostclassifier__n_estimators': [20, 50, 100, 200]
        }
    }
]

def binary_mapper(grade):
    if (grade >= grade_cutoff):
        return 1
    return 0
    
def resample_df(df, samples, random_state = 0):
    df = df[samples]
    df = pd.get_dummies(df, columns=df.select_dtypes(include=['object']).keys())
    df = df.sample(frac=1, random_state = random_state) # Shuffles the dataframe
    # df.loc['percent_grade'] = df.percent_grade.fillna(0)
    df = df.dropna(subset=['percent_grade'])
    return df

def get_param_string(score_df, param_grid):
    keys = ["param_"+key for key in param_grid.keys()]
    param_values = [key.split("__")[1]+"_"+score_df[key].apply(str) for key in keys]
    return ["__".join(tup) for tup in zip(*param_values)]
    
def fit_df(df, estimator, param_grid, name, random_state=0):
    # print([key for key in df.keys()])
    X = df.drop(columns=['percent_grade', 'user_id', 'course_id_course-v1:GTx+ISYE6501x+3T2018'])
    y = df['percent_grade'] > grade_cutoff
    cv = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=random_state)
    pipe = make_pipeline(imp_mean, scaler, estimator)
    search = GridSearchCV(pipe, param_grid, scoring='roc_auc', iid=False, cv=cv,
                          return_train_score=False)
    search.fit(X, y)
    score_df = pd.DataFrame(search.cv_results_)
    score_df['params'] = get_param_string(score_df, param_grid)

    score_df = score_df.set_index('params')
    keys = ["split%i_test_score" % key for key in range(n_folds)]
    score_df = score_df[keys].rename_axis('fold', axis='columns')
    return score_df.stack().rename('ROC-AUC')
    
def get_scores(df, estimator, sample, random_state):
    new_df = resample_df(df, sample, random_state)
    score_df = fit_df(new_df, estimator['value'], estimator['parameters'], estimator['name'], random_state+1)
    return score_df 

def getseconds(str):
    separated = str.split(" ")
    accumulator = 0
    if len(separated) == 3:
        accumulator += ((int)(separated[0])) * 24 * 60 * 60
    second_separated = separated[-1].split(":")
    accumulator += (int)(second_separated[0]) * 60 * 60
    accumulator += (int)(second_separated[1]) * 60
    accumulator += (int)(second_separated[2])
    return accumulator

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_models.py <.csv file>")
        return 0

    df = pd.read_csv(sys.argv[1])
    df = df.fillna(0)

    df = df.drop(columns=["passed"])

    samples = {'all': [key for key in df.keys()]}

    for estimator, sample, seed in itertools.product(estimators, samples.keys(), seeds):
        scores = get_scores(df, estimator, samples[sample], seed).reset_index()
        scores['model'] = estimator['name']
        scores['seed'] = seed
        scores['sample'] = sample
        df = df.append(scores)
    df.to_csv("model_results.csv", index=False)
    print("Done!")
    
main()