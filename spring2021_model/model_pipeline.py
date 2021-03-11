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

def clean_data_null(df):
    return df.dropna();
    

def clean_data_outlier(df_in):
   return df_in

def transform_data(df_in):
	# Add each Event Type as a columns.
    df_in["event_type"].replace({"edx.bi.course.upgrade.sidebarupsell.displayed": "sidebar", "edx.ui.lms.link_clicked": "hypertext", "edx.course.tool.accessed": "tool_accessed","edx.video.closed_captions.hidden": "captions_hidden", "edx.video.closed_captions.shown": "captions_shown", "edx.ui.lms.sequence.next_selected": "next_selected", "edx.course.home.resume_course.clicked": "resume_course"}, inplace=True)
    new_data = df_in.pivot_table('count', ['course_id', 'user_id','week'], 'event_type')
    new_data.reset_index( drop=False, inplace=True )
    return new_data

def explore_unsupervised(data):
    del data['user_id']
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
    plt.savefig('./plots/kmeans.png') 
    plt.clf()
    scores = [KMeans(n_clusters=i+2).fit(normalized_vectors).inertia_ for i in range(10)]
    sns.lineplot(np.arange(2, 12), scores)
    plt.xlabel('Number of clusters')
    plt.ylabel("Inertia")
    plt.title("Inertia of Cosine k-Means versus number of clusters")
    plt.savefig('./plots/kmeans_cosine.png') 
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
    plt.savefig("./plots/clustering_results.png")


def feature_explortion(data):
    '''
    Explore features and return a list of features thats needs to be included in the model
    '''
    print("Data size: " + str(data.shape))
    #English does not have good data, hence removing
    plot_feature(data,'gender','barh')
    plot_feature(data,'country','barh')
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
    features = cm.index[1:16].tolist()
    data[np.array(features)].hist(bins=200,figsize=(16,8))
    plt.savefig('./plots/best_features.png') 
    return features

def plot_feature(data, column, style):
    data_count=len(data.index)
    plt.clf()
    ax=data[column].value_counts(sort=False).sort_index().plot(kind=style)
    if style == 'barh':
        for p in ax.patches:
            ax.annotate(str(round(p.get_width()/data_count * 100,2)) +" %", (p.get_x() + p.get_width(), p.get_y()), xytext=(5, 10), textcoords='offset points')
    plt.savefig('./plots/' +column + '.png') 

def runAnalysisForAggregatedData(data):
    agg_data = data.groupby(
    ['user_id']
    ).agg(
         weeks_active=('week', 'count'),    # Sum duration per group
         gender= ('gender', 'first'),
         country=('country', 'first'),
         year_of_birth=('year_of_birth', 'first'),
         level_of_education=('level_of_education', 'first'),
		 page_close_agg_count=('page_close', 'mean'),
         hypertext_agg_count=('hypertext', 'mean'),
         next_selected_agg_count=('next_selected', 'mean'),
         resume_course_agg_count=('resume_course', 'mean'),
         sidebar_agg_count=('sidebar', 'mean'),
		 seq_goto_agg_count=('seq_goto', 'mean'),
         seq_next_agg_count=('seq_next', 'mean'),
         seq_prev_agg_count=('seq_prev', 'mean'),
         tool_accessed_agg_count=('tool_accessed', 'mean'),
         problem_check_agg_count=('problem_check', 'mean'),
         problem_graded_agg_count=('problem_graded', 'mean'),
         seek_video_agg_count=('seek_video', 'mean'),
         load_video_agg_count=('load_video', 'mean'),
         play_video_agg_count=('play_video', 'mean'),
		 pause_video_agg_count=('pause_video', 'mean'),
         stop_video_agg_count=('stop_video', 'mean'),
         captions_hidden_agg_count=('captions_hidden', 'mean'),
         captions_shown_agg_count=('captions_shown', 'mean'),
         hide_transcript_agg_count=('hide_transcript', 'mean'),
         show_transcript_agg_count=('show_transcript', 'mean'),
         speed_change_video_agg_count=('speed_change_video', 'mean'),
         percent_progress=('percent_grade', 'first')
    )
    agg_data.reset_index(inplace=True)
    agg_data['user_id'] = agg_data['user_id'].astype(int) 
    #test1.columns = test1.columns.get_level_values(0)
    #print(test1.columns)
    explore_unsupervised(agg_data.copy())
    xVars = feature_explortion(agg_data)
    #print(agg_data.head())

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
    data = clean_data_null(data)
    print("Data Shape without Nulls: ", data.shape)
    #clean_data_outlier(data)
    #print(data.event_type.unique())
    data = transform_data(data)
    data= data.replace(np.nan,0)
    data = pd.merge(data, demog, on="user_id")
    data = pd.merge(data, output, on="user_id")
    data.drop(columns=['course_id'], inplace=True)
    runAnalysisForAggregatedData(data)

    
if __name__ == "__main__":
    main()