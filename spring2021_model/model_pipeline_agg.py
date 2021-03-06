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
import joblib


output_variable = "percent_progress"
filter_best_correlated = True


def explore_unsupervised_agg(data, course):
    #del data['user_id']
    # Temp drop all na value
    data = data.dropna(axis=0)
   
    others_categorical = ['gender','level_of_education','country']
    for i in others_categorical:
        data = data.join(pd.get_dummies(data[i], prefix=i))
    data.drop(others_categorical, axis=1, inplace=True)
    otput = data["percent_progress"]
    unsupervised_df = data.drop(["percent_progress"], 1, inplace=False)
    normalized_vectors = preprocessing.normalize(unsupervised_df)
    scores = [KMeans(n_clusters=i+2).fit(unsupervised_df).inertia_ for i in range(10)]
    sns.lineplot(np.arange(2, 12), scores)
    plt.xlabel('Number of clusters')
    plt.ylabel("Inertia")
    plt.title("Inertia of k-Means versus number of clusters")
    plt.savefig('./plots/' +course + '/kmeans.png') 
    plt.clf()
    scores = [KMeans(n_clusters=i+2).fit(normalized_vectors).inertia_ for i in range(10)]
    sns.lineplot(np.arange(2, 12), scores)
    plt.xlabel('Number of clusters')
    plt.ylabel("Inertia")
    plt.title("Inertia of Cosine k-Means versus number of clusters")
    plt.savefig('./plots/' + course + '/kmeans_cosine.png') 
    kmeans = KMeans(n_clusters=3).fit(unsupervised_df)

    normalized_kmeans = KMeans(n_clusters=3).fit(normalized_vectors)

    #min_samples = unsupervised_df.shape[1]+1
    #dbscan = DBSCAN(eps=3.5, min_samples=min_samples).fit(unsupervised_df)
    print('kmeans: {}'.format(silhouette_score(unsupervised_df, kmeans.labels_, metric='euclidean')))
    print('Cosine kmeans: {}'.format(silhouette_score(normalized_vectors, normalized_kmeans.labels_, metric='cosine')))
    #print('DBSCAN: {}'.format(silhouette_score(unsupervised_df, dbscan.labels_, metric='cosine')))
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(unsupervised_df))
    df_scaled.columns = unsupervised_df.columns
    df_scaled['cluster'] = normalized_kmeans.labels_
    data['cluster'] = normalized_kmeans.labels_
    print(data.groupby('cluster')['percent_progress'].mean())

    # Calculate variables with largest differences (by standard deviation)
    # The higher the standard deviation in a variable based on average values for each cluster
    # The more likely that the variable is important when creating the cluster
    df_mean = df_scaled.loc[df_scaled.cluster!=-1, :].groupby('cluster').mean().reset_index()
    results = pd.DataFrame(columns=['Variable', 'Std'])
    for column in df_mean.columns[1:]:
        results.loc[len(results), :] = [column, np.std(df_mean[column])]
    selected_columns = list(results.sort_values('Std', ascending=False).head(7).Variable.values) + ['cluster']

    # Plot data
    tidy = df_scaled[selected_columns].melt(id_vars='cluster')
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.barplot(x='cluster', y='value', hue='variable', data=tidy, palette='Set3')
    plt.legend(loc='upper right')
    plt.savefig("./plots/" + course + "/clustering_results.png")


def feature_exploration_agg(data, course):
    '''
    Explore features and return a list of features thats needs to be included in the model
    '''
    print("Data size: " + str(data.shape))
    #English does not have good data, hence removing
    plot_feature_agg(data,'gender','barh', course)
    plot_feature_agg(data,'country','barh',course)
    plot_feature_agg(data,'level_of_education','barh',course)
    plot_feature_agg(data,'percent_progress','line',course)
    print(data['percent_progress'].describe())
	
    corr_matrix = data.corr()
    fig, ax = plt.subplots(figsize=(18,18)) 
    sns_plot = sns.heatmap(corr_matrix, 
            xticklabels=corr_matrix.columns.values,
            yticklabels=corr_matrix.columns.values,
            ax=ax)
    sns_plot.figure.savefig("./plots/" + course + "/correlation.png")
    cm=corr_matrix[output_variable].sort_values(ascending=False)
    features = cm.index[1:16].tolist()
    data[np.array(features)].hist(bins=200,figsize=(16,8))
    plt.savefig('./plots/' + course + '/best_features.png') 
    return features

def plot_feature_agg(data, column, style, course):
    data_count=len(data.index)
    plt.clf()
    ax=data[column].value_counts(sort=False).sort_index().plot(kind=style)
    if style == 'barh':
        for p in ax.patches:
            ax.annotate(str(round(p.get_width()/data_count * 100,2)) +" %", (p.get_x() + p.get_width(), p.get_y()), xytext=(5, 10), textcoords='offset points')
    plt.savefig('./plots/' +course + '/'+column + '.png') 

def runAnalysisForAggregatedData(data, course):
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
    agg_data = agg_data[agg_data['load_video_agg_count'] + agg_data['play_video_agg_count']!=0 ]
    agg_data = agg_data[agg_data['percent_progress'] != 0]
    #write_csv('./data/', agg_data, 'MGT100')
    agg_data.drop(['user_id'], axis=1, inplace=True)
    #agg_data['user_id'] = agg_data['user_id'].astype(int) 
    #test1.columns = test1.columns.get_level_values(0)
    #print(test1.columns)
    print("Running Aggregated Clusterening analysis..............")
    explore_unsupervised_agg(agg_data.copy(), course)
    print("Running Aggregated Null analysis..............")
    agg_data=clean_agg_data_null(agg_data, course)
    print("Running Aggregated Outlier analysis..............")
    agg_data=clean_agg_data_outlier(agg_data, course)
    print("Running Aggregated Feature analysis..............")
    xVars = feature_exploration_agg(agg_data, course)
    X = agg_data.drop([output_variable], axis=1)
    y = agg_data[output_variable]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.90,test_size=0.10, random_state=2020)
    train_data = X_train.copy()
    train_data[output_variable] = y_train
    if(filter_best_correlated):
	    preprocessor = preprocessor_best_features_agg(xVars)
    else:
        preprocessor = preprocessor_categorical_agg()
    print("Running Aggregated Model analysis..............")
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
        {
            'estimator':DecisionTreeRegressor(), 
		    'params':{
                'regressor__max_depth':np.arange(2, 6),
                'regressor__min_samples_leaf':np.arange(1,15),
                #'regressor__max_leaf_nodes':(6,7,8) - R default setting found 7 leaf nodes but looks like there is a better configuration hence adding them for tuning.
             }
        },
        {
            'estimator':RandomForestRegressor(n_estimators=1000), 
		    'params':{
                'regressor__max_depth':np.arange(5, 6),
                'regressor__min_samples_leaf':np.arange(14,15)
             }
        },
        {
            'estimator':BaggingRegressor(DecisionTreeRegressor(), random_state=2020), 
		    'params':{
                'regressor__base_estimator__max_depth':np.arange(4, 5),
                'regressor__base_estimator__min_samples_leaf':np.arange(14,15),
                'regressor__n_estimators':(50,200)
             }
        },
        {
            'estimator':AdaBoostRegressor(DecisionTreeRegressor(), random_state=2020), 
            'params':{
                'regressor__base_estimator__max_depth':np.arange(4, 5),  
                'regressor__base_estimator__min_samples_leaf':np.arange(19, 20), 
                'regressor__loss':('linear', 'square', 'exponential'),
                'regressor__n_estimators':(50, 100), 
                'regressor__learning_rate':(0.01,0.05)
             }
        },
        {
            'estimator':MLPRegressor(random_state=2020),  
            'params':{
                'regressor__hidden_layer_sizes':np.arange(9, 10), 
                'regressor__activation':('tanh', 'relu'), 
                'regressor__solver':('sgd', 'adam'),
                'regressor__max_iter':(100,200)
            } 
        },
        {
            'estimator':KNeighborsRegressor(),  
            'params':{'regressor__n_neighbors':np.arange(10, 15)}
        },
		{
            'estimator':GradientBoostingRegressor(), 
            'params':{
                'regressor__max_depth':np.arange(5, 6), 
                'regressor__min_samples_leaf':np.arange(1, 2),
                'regressor__n_estimators':(50,300), 
                'regressor__learning_rate':(0.05,0.1)
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
        best_model, train_score, test_score = quick_eval_agg(pipe, X_train, y_train, X_test, y_test, r['params'])
        if(filter_best_correlated):
            plot_best_features_agg(best_model, xVars, course)
        if(train_score<max_score):
            max_score=train_score
            final_model=best_model    
        rows.append([r['estimator'].__class__.__name__, train_score, test_score])
    joblib.dump(final_model, './model/' + course + '/best_model.pkl')
    output = pd.DataFrame(rows, columns=["Algorithm", "Train RMSE", "Test RMSE"])
    output = output.set_index("Algorithm")
    print(output)
    fig = output.plot(kind='barh').get_figure()
    fig.savefig('./plots/' +course + '/model_plots/algorithms.png',bbox_inches='tight')

def quick_eval_agg(pipeline, X_train, y_train, X_test, y_test, params, verbose=True):
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


def clean_agg_data_null(df,course):
    print(df.isnull().sum().sort_values(ascending=False))

    #fill null in education and gender with unspecified
    df['level_of_education'].fillna('not specified', inplace=True)
    df['gender'].fillna('not specified', inplace=True)
    df['country'].fillna('not specified', inplace=True)

    #Filling in year_of_birth col with median, creating box plot of before and after
    ax = df.boxplot(column='year_of_birth')
    ax.figure.savefig("./plots/"+ course + "/YOB_boxplot_before.png")
    ax.figure.clf()

    df['year_of_birth'].fillna(df['year_of_birth'].median(), inplace=True);
    ax = df.boxplot(column='year_of_birth')
    ax.figure.savefig("./plots/"+ course + "/YOB_boxplot_after.png")
    ax.figure.clf()

    #create bar graphs of the averages of the output variable and the 6 top input variables as seperated by gender, US, and percent progress
    cols = ['percent_progress', 'hypertext_agg_count', 'load_video_agg_count', 'next_selected_agg_count', 'page_close_agg_count', 'problem_check_agg_count', 'problem_graded_agg_count'];

    for col in cols:

        genderPlot = (df.groupby('gender')[col].mean()).plot.bar()
        genderPlot.axhline(df[col].mean(), color='red', linewidth=2)
        genderPlot.figure.savefig("./plots/" + course + "/gender_vs_"+col+".png")
        genderPlot.figure.clf()
        USplot = (df.fillna(-1).groupby(by='country')[col].mean()).plot.bar()
        USplot.axhline(df[col].mean(), color='red', linewidth=2)
        USplot.figure.savefig("./plots/" + course + "/country_vs_"+col+".png")
        USplot.figure.clf()
        
        LOEplot = (df.groupby('level_of_education')[col].mean()).plot.bar()
        LOEplot.axhline(df[col].mean(), color='red', linewidth=2)
        LOEplot.figure.savefig("./plots/" + course + "/level_of_education_vs_"+col+".png")
        LOEplot.figure.clf()

    return df;


def clean_agg_data_outlier(df_in, course):
   df=df_in.copy()
   df = df.set_index('percent_progress')
   #del df['English']
   del df['country']
   #del df['Age']
   df["level_of_education"]=df["level_of_education"].fillna("Not Specified")
   # Temp drop all na value
   df = df.dropna(axis=0)
   #plot indivisual variable to obsere outlier
   sns.boxplot(df["year_of_birth"])
   #This method only remove outlier for numerical independent variable
   del df ["level_of_education"]
   del df ["gender"]
   df['Age'] = pd.datetime.now().year - df.year_of_birth
   del df ["year_of_birth"]
   #remove outlier based on z-score
   #remove outlier
   z_scores = stats.zscore(df)
   abs_z_scores = np.abs(z_scores)
   filtered_entries = (abs_z_scores < 2).all(axis=1)
   filtered_df = df_in[filtered_entries]
   #plot again to see if it works
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

def preprocessor_best_features_agg(features):
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

def preprocessor_categorical_agg():
    categorical = ColumnTransformer(
    [
        ("categorical",  OneHotEncoder(dtype=np.int),['gender','level_of_education']),
    ],
    remainder="passthrough",
    )
    return categorical

def plot_best_features_agg(estimator, xVars, course):
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
        plt.savefig('./plots/' + course+ '/model_plots/' +estimator.named_steps['regressor'].__class__.__name__ + '.png')  
