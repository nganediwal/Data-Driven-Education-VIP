import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.model_selection as model_selection
from sklearn import preprocessing
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Lasso, Ridge, LassoLars
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import MinMaxScaler	
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

def clean_data(df):
    del df['English']
    #del df['US']
    df["level_of_education"]=df["level_of_education"].fillna("Not Specified")


    # Temp drop all na value
    df = df.dropna(axis=0)

    #plot indivisual variable to obsere outlier
    sns_plot=sns.boxplot(df["year_of_birth"])
    sns_plot.figure.savefig("./plots/yob_before.png")

    # Create z-score columns of all numerical variables
    df2 = df.copy()

    z_column = list(df.columns)
    z_column .remove('gender')
    z_column .remove('level_of_education')
    print(df2[z_column])

    for col in z_column:
        col_zscore = col + '_zscore'
        df2[col_zscore] = (df2[col] - df2[col].mean())/df2[col].std(ddof=0)
    
    #drop rows with z-score higher than 3 or lower than -3

    for col in z_column:
        df2.drop(df2[df2[col] < -3].index, inplace = True)
        df2.drop(df2[df2[col] > 3].index, inplace = True) 


    #plot numerical variable to see if we seccefully removed outliers
    sns_plot=sns.boxplot(df2["year_of_birth"])
    sns_plot.figure.savefig("./plots/yob_after.png")

    #create dummy for gender

    df2["gender"]=df2["gender"].fillna("Not Specified")
    dummiesgender = pd.get_dummies(df2['gender']).rename(columns=lambda x: 'gender_' + str(x))
    df = pd.concat([df, dummiesgender], axis=1)
    return df

def explore_unsupervised(data):
    del data['English']
    # Temp drop all na value
    data = data.dropna(axis=0)
   
    others_categorical = ['gender','year_of_birth','level_of_education','US']
    for i in others_categorical:
        data = data.join(pd.get_dummies(data[i], prefix=i))
    data.drop(others_categorical, axis=1, inplace=True)

    #plot_income = sns.distplot(normalized_vectors["percent_progress"])
    #plot_spend = sns.distplot(normalized_vectors["load_video_agg_count"])
    #plt.xlabel('percent_progress / load_video_agg_count')
    #plt.savefig('./plots/curves.png') 
    #plt.clf()
    unsupervised_df = data.drop(["percent_progress"], 1, inplace=False)
    normalized_vectors = preprocessing.normalize(unsupervised_df)
    scores = [KMeans(n_clusters=i+2).fit(unsupervised_df).inertia_ for i in range(10)]
    sns.lineplot(np.arange(2, 12), scores)
    plt.xlabel('Number of clusters')
    plt.ylabel("Inertia")
    plt.title("Inertia of k-Means versus number of clusters")
    plt.savefig('./plots/kmeans.png') 
    plt.clf()
    #normalized_vectors = preprocessing.normalize(unsupervised_df)
    scores = [KMeans(n_clusters=i+2).fit(normalized_vectors).inertia_ for i in range(10)]
    sns.lineplot(np.arange(2, 12), scores)
    plt.xlabel('Number of clusters')
    plt.ylabel("Inertia")
    plt.title("Inertia of Cosine k-Means versus number of clusters")
    plt.savefig('./plots/kmeans_cosine.png') 
    kmeans = KMeans(n_clusters=4).fit(unsupervised_df)

    #normalized_vectors = preprocessing.normalize(df)
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

def feature_explortion(data):
    '''
    Explore features and return a list of features thats needs to be included in the model
    '''
    print("Data size: " + str(data.shape))
    #English does not have good data, hence removing
    #data= data.drop(columns=['English'])
    plot_feature(data,'gender','barh')
    plot_feature(data,'US','barh')
    plot_feature(data,'level_of_education','barh')
    plot_feature(data,'percent_progress','line')
    print(data['percent_progress'].describe())
	

    #plot_feature_combo(plotting_data,'level_of_education', 'percent_progress','bar')
    #plot_feature_combo(plotting_data,'gender', 'percent_progress','bar')
    #print("--------------------play_video---------------")
    #print(data.groupby('level_of_education').play_video_agg_count.mean())
    #print(data.groupby('US').play_video_agg_count.mean())
    #print(data.groupby('gender').play_video_agg_count.mean())

    #print("--------------------problem_graded---------------")
    #print(data.groupby('level_of_education').problem_graded_agg_count.mean())
    #print(data.groupby('US').problem_graded_agg_count.mean())
    #print(data.groupby('gender').problem_graded_agg_count.mean())

    #print("--------------------percent_progress---------------")
    #print(data.groupby('level_of_education').percent_progress.mean())
    #print(data.groupby('US').percent_progress.mean())
    #print(data.groupby('gender').percent_progress.mean())
	#df.plot(x='col_name_1', y='col_name_2', style='o')
	#df.groupby('Gender').Age.mean()
    #data['video_interation'] = data['seek_video_agg_count'] + data['load_video_agg_count'] +  data['play_video_agg_count'] +  data['pause_video_agg_count'] +  data['stop_video_agg_count']
    #data['problem_interaction'] = data['problem_check_agg_count'] + data['problem_graded_agg_count']
    #print(data.groupby('US').video_interation.mean())
    #print(data.groupby('level_of_education').video_interation.mean())
    #print(data.groupby('level_of_education').problem_interaction.mean())
    #data= data.drop(columns=['video_interation'])
    #data= data.drop(columns=['problem_interaction'])
    #print(data.isnull().sum().sort_values(ascending=False))
    corr_matrix = data.corr()
    fig, ax = plt.subplots(figsize=(18,18)) 
    sns_plot = sns.heatmap(corr_matrix, 
            xticklabels=corr_matrix.columns.values,
            yticklabels=corr_matrix.columns.values,
            ax=ax)
    sns_plot.figure.savefig("./plots/correlation.png")
    cm=corr_matrix[output_variable].sort_values(ascending=False)
    features = cm.index[1:2].tolist()
    data[np.array(features)].hist(bins=200,figsize=(16,8))
    plt.savefig('./plots/best_features.png') 
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
    #explore_unsupervised(data.copy())
    #data=clean_data(data.copy())
    xVars = feature_explortion(data)
    X = data.drop([output_variable], axis=1)
    y = data[output_variable]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.75,test_size=0.25, random_state=2020)
    train_data = X_train.copy()
    train_data[output_variable] = y_train
    preprocessor = preprocessor_pipe(xVars)
    pca = PCA()
    regressors = [
        LinearRegression(),
        Lasso(alpha=.5),
        Ridge(alpha=.1),
        LassoLars(alpha=.1),
        DecisionTreeRegressor(),
        RandomForestRegressor(n_estimators=100),
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