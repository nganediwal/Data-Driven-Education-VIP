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
filter_best_correlated = False

def read_csv(filepath):
    
    '''
    Return course data
    '''

    #Columns in events.csv - patient_id,event_id,event_description,timestamp,value
    data = pd.read_csv(filepath + 'course_data.csv')

    return data


def quick_eval(pipeline, X_train, y_train, X_test, y_test, params, verbose=True):
    """
    Quickly trains modeling pipeline and evaluates on test data.      Returns original model, training RMSE, and testing
    RMSE as a tuple.
    """
    CV = GridSearchCV(pipeline, params, scoring = 'neg_mean_absolute_error', n_jobs= 6, cv=10)
    CV.fit(X_train, y_train)
    #if the estimator has an option to provide best features, plot it
    #if(hasattr(CV.best_estimator_.named_steps['regressor'], 'feature_importances_')):
    #    plt.figure(figsize=(18,18))
    #    feat_imp = pd.Series(CV.best_estimator_.named_steps['regressor'].feature_importances_).sort_values(ascending=False)
    #    feat_imp.plot(kind='bar', title='Feature Importances')
    #    plt.clf()
    #    plt.ylabel('Feature Importance Score')
    #    importances = pipeline.named_steps['regressor'].feature_importances_
    #    feature_size=importances.shape[0]
    #    indices = np.argsort(importances)[::-1]
    #    plt.figure()
    #    plt.title("Feature importances")
    #    plt.bar(range(feature_size), importances[indices],align="center")
    #    plt.xticks(range(feature_size), indices)
    #    plt.xlim([-1, feature_size])
    #    plt.savefig('./plots/model_plots/' +pipeline.named_steps['regressor'].__class__.__name__ + '.png')  
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

def plot_feature(data, column, style):
    data_count=len(data.index)
    plt.clf()
    ax=data[column].value_counts(sort=False).sort_index().plot(kind=style)
    if style == 'barh':
        for p in ax.patches:
            ax.annotate(str(round(p.get_width()/data_count * 100,2)) +" %", (p.get_x() + p.get_width(), p.get_y()), xytext=(5, 10), textcoords='offset points')
    plt.savefig('./plots/' +column + '.png') 

def plot_feature_combo(data, column1, column2, style):
    data_count=len(data.index)
    plt.clf()
    data.plot(x=column1, y=column2, kind=style)
    plt.savefig('./plots/' +column1 +'_'+ column2 + '.png') 



def clean_data_null(df):
    print(df.isnull().sum().sort_values(ascending=False))

    #drop English col
    df.drop(columns=['English'], inplace=True)


    #fill null in education and gender with unspecified
    df['level_of_education'].fillna('not specified', inplace=True)
    df['gender'].fillna('not specified', inplace=True)
    df['US'].fillna(-1, inplace=True)

    #Filling in year_of_birth col with median, creating box plot of before and after
    ax = df.boxplot(column='year_of_birth')
    ax.figure.savefig("./plots/YOB_boxplot_before.png")
    ax.figure.clf()

    df['year_of_birth'].fillna(df['year_of_birth'].median(), inplace=True);
    ax = df.boxplot(column='year_of_birth')
    ax.figure.savefig("./plots/YOB_boxplot_after.png")
    ax.figure.clf()

    #create bar graphs of the averages of the output variable and the 6 top input variables as seperated by gender, US, and percent progress
    cols = ['percent_progress', 'hypertext_agg_count', 'load_video_agg_count', 'next_selected_agg_count', 'page_close_agg_count', 'problem_check_agg_count', 'problem_graded_agg_count'];

    for col in cols:

        genderPlot = (df.groupby('gender')[col].mean()).plot.bar()
        genderPlot.axhline(df[col].mean(), color='red', linewidth=2)
        genderPlot.figure.savefig("./plots/gender_vs_"+col+".png")
        genderPlot.figure.clf()
        USplot = (df.fillna(-1).groupby(by='US')[col].mean()).plot.bar()
        USplot.axhline(df[col].mean(), color='red', linewidth=2)
        USplot.figure.savefig("./plots/US_vs_"+col+".png")
        USplot.figure.clf()
        
        LOEplot = (df.groupby('level_of_education')[col].mean()).plot.bar()
        LOEplot.axhline(df[col].mean(), color='red', linewidth=2)
        LOEplot.figure.savefig("./plots/level_of_education_vs_"+col+".png")
        LOEplot.figure.clf()

    return df;
    

def explore_unsupervised(data):
    del data['English']
    # Temp drop all na value
    data = data.dropna(axis=0)
   
    others_categorical = ['gender','year_of_birth','level_of_education','US']
    for i in others_categorical:
        data = data.join(pd.get_dummies(data[i], prefix=i))
    data.drop(others_categorical, axis=1, inplace=True)
    unsupervised_df = data.drop(["percent_progress"], 1, inplace=False)
    normalized_vectors = preprocessing.normalize(unsupervised_df)
    scores = [KMeans(n_clusters=i+2).fit(unsupervised_df).inertia_ for i in range(10)]
    sns.lineplot(np.arange(2, 12), scores)
    plt.xlabel('Number of clusters')
    plt.ylabel("Inertia")
    plt.title("Inertia of k-Means versus number of clusters")
    plt.savefig('./plots/kmeans.png') 
    plt.clf()
    scores = [KMeans(n_clusters=i+2).fit(normalized_vectors).inertia_ for i in range(10)]
    sns.lineplot(np.arange(2, 12), scores)
    plt.xlabel('Number of clusters')
    plt.ylabel("Inertia")
    plt.title("Inertia of Cosine k-Means versus number of clusters")
    plt.savefig('./plots/kmeans_cosine.png') 
    kmeans = KMeans(n_clusters=4).fit(unsupervised_df)

    normalized_kmeans = KMeans(n_clusters=4).fit(normalized_vectors)

    min_samples = unsupervised_df.shape[1]+1
    dbscan = DBSCAN(eps=3.5, min_samples=min_samples).fit(unsupervised_df)
    print('kmeans: {}'.format(silhouette_score(unsupervised_df, kmeans.labels_, metric='euclidean')))
    print('Cosine kmeans: {}'.format(silhouette_score(normalized_vectors, normalized_kmeans.labels_, metric='cosine')))
    print('DBSCAN: {}'.format(silhouette_score(unsupervised_df, dbscan.labels_, metric='cosine')))
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(unsupervised_df))
    df_scaled.columns = unsupervised_df.columns
    df_scaled['dbscan'] = dbscan.labels_
    df_scaled['percent_progress'] = unsupervised_df["percent_progress"]
    print(df_scaled)

    # Calculate variables with largest differences (by standard deviation)
    # The higher the standard deviation in a variable based on average values for each cluster
    # The more likely that the variable is important when creating the cluster
    df_mean = df_scaled.loc[df_scaled.dbscan!=-1, :].groupby('dbscan').mean().reset_index()
    results = pd.DataFrame(columns=['Variable', 'Std'])
    for column in df_mean.columns[1:]:
        results.loc[len(results), :] = [column, np.std(df_mean[column])]
    selected_columns = list(results.sort_values('Std', ascending=False).head(7).Variable.values) + ['dbscan']

    # Plot data
    tidy = df_scaled[selected_columns].melt(id_vars='dbscan')
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.barplot(x='dbscan', y='value', hue='variable', data=tidy, palette='Set3')
    plt.legend(loc='upper right')
    plt.savefig("./plots/dbscan_results.png")

def clean_data_outlier(df_in):
   df=df_in.copy()
   df = df.set_index('percent_progress')
   #del df['English']
   del df['US']
   #del df['Age']
   df["level_of_education"]=df["level_of_education"].fillna("Not Specified")
   # Temp drop all na value
   df = df.dropna(axis=0)
   #plot indivisual variable to obsere outlier
   sns.boxplot(df["year_of_birth"])
   #This method only remove outlier for numerical independent variable
   del df ["level_of_education"]
   del df ["gender"]

   #remove outlier based on z-score
   #remove outlier
   z_scores = stats.zscore(df)
   abs_z_scores = np.abs(z_scores)
   filtered_entries = (abs_z_scores < 2).all(axis=1)
   filtered_df = df_in[filtered_entries]
   #plot again to see if it works
   sns.boxplot(filtered_df["year_of_birth"])
   #create outlier table for outlier analysis
   for col in df:
       col_zscore = col + '_zscore'
       df[col_zscore] = (abs((df[col] - df[col].mean())/df[col].std(ddof=0))>2)*1
   z_cols = [col for col in df.columns if 'zscore' in col]
   df_outlier= pd.DataFrame() 
   for col in z_cols:
       df_outlier[col]= df[col]
   #plots are created separately and are available in the plots folder
   return filtered_df



	      
def feature_explortion(data):
    '''
    Explore features and return a list of features thats needs to be included in the model
    '''
    print("Data size: " + str(data.shape))
    #English does not have good data, hence removing
    plot_feature(data,'gender','barh')
    plot_feature(data,'US','barh')
    plot_feature(data,'level_of_education','barh')
    plot_feature(data,'percent_progress','line')
    print(data['percent_progress'].describe())
	
    corr_matrix = data.corr()
    fig, ax = plt.subplots(figsize=(18,18)) 
    sns_plot = sns.heatmap(corr_matrix, 
            xticklabels=corr_matrix.columns.values,
            yticklabels=corr_matrix.columns.values,
            ax=ax)
    sns_plot.figure.savefig("./plots/correlation.png")
    cm=corr_matrix[output_variable].sort_values(ascending=False)
    features = cm.index[1:5].tolist()
    data[np.array(features)].hist(bins=200,figsize=(16,8))
    plt.savefig('./plots/best_features.png') 
    return features

def preprocessor_best_features(features):
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

def preprocessor_categorical():
    categorical = ColumnTransformer(
    [
        ("categorical",  OneHotEncoder(dtype=np.int),['gender','level_of_education']),
    ],
    remainder="passthrough",
    )
    return categorical

def main():
    data_path = './data/'
    data=read_csv(data_path)
    #explore_unsupervised(data.copy())
    data=clean_data_null(data)
    data=clean_data_outlier(data)
    xVars = feature_explortion(data)
    X = data.drop([output_variable], axis=1)
    y = data[output_variable]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.75,test_size=0.25, random_state=2020)
    train_data = X_train.copy()
    train_data[output_variable] = y_train
    if(filter_best_correlated):
	    preprocessor = preprocessor_best_features(xVars)
    else:
        preprocessor = preprocessor_categorical()
    regressors = [
        # @Rachel
        #LinearRegression(),
        {
            'estimator':LinearRegression(),
            'params':{
                'regressor__fit_intercept': (True, False),
                'regressor__normalize': (True, False),
			}
		},
        #Lasso
        {
            'estimator':Lasso(),
            'params':{
                'regressor__alpha': (.01, .05, .1, .25, .5),
                'regressor__fit_intercept': (True, False),
                'regressor__normalize': (True, False)
			}
		},
        # @Mia
        #DecisionTreeRegressor(),
        #RandomForestRegressor(n_estimators=100),
        {
            'estimator':BaggingRegressor(DecisionTreeRegressor(), random_state=2020), 
		    'params':{
                'regressor__base_estimator__max_depth':np.arange(4, 6),
                'regressor__base_estimator__min_samples_leaf':np.arange(5, 15),
                'regressor__n_estimators':(100, 200)
             }
        },
        {
            'estimator':AdaBoostRegressor(DecisionTreeRegressor(), random_state=2020), 
            'params':{
                'regressor__base_estimator__max_depth':np.arange(4, 6),  
                'regressor__base_estimator__min_samples_leaf':np.arange(15, 20), 
                'regressor__loss':('linear', 'square', 'exponential'),
                'regressor__n_estimators':(100, 200), 
                'regressor__learning_rate':(0.01, 0.05)
             }
        },
        {
            'estimator':MLPRegressor(random_state=2020),  
            'params':{
                'regressor__hidden_layer_sizes':np.arange(10, 15), 
                'regressor__activation':('tanh', 'relu'), 
                'regressor__solver':('sgd', 'adam'),
                'regressor__max_iter':(100,200)
            } 
        },
        {
            'estimator':KNeighborsRegressor(),  
            'params':{'regressor__n_neighbors':np.arange(1, 15)}
        },
		{
            'estimator':GradientBoostingRegressor(), 
            'params':{
                'regressor__max_depth':np.arange(4, 6), 
                'regressor__min_samples_leaf':np.arange(1, 5),
                'regressor__n_estimators':(100,300), 
                'regressor__learning_rate':(0.1, 0.5)
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
        if(train_score<max_score):
            max_score=train_score
            final_model=best_model    
        rows.append([r['estimator'].__class__.__name__, train_score, test_score])
    joblib.dump(final_model, './model/best_model.pkl')
    output = pd.DataFrame(rows, columns=["Algorithm", "Train RMSE", "Test RMSE"])
    output = output.set_index("Algorithm")
    print(output)
    fig = output.plot(kind='barh').get_figure()
    fig.savefig('./plots/model_plots/algorithms.png',bbox_inches='tight')
if __name__ == "__main__":
    main()