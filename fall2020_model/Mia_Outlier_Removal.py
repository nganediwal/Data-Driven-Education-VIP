import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_excel
import seaborn as sns
from scipy import stats

df = pd.read_excel('MOOC_course data VIP-V2.xlsx', sep=',')
df = df.set_index('percent_progress')
del df['English']
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
filtered_df = df[filtered_entries]
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
df_outlier

#for the non-numerical factors, My plan is to create dummy variables, run the regression model 
#and plot cook's distance to observe and remove outlier >1 but I don't know how to do it in Python... 
#So I worked in R, I would keep learning how to do it in python and update this script later this weekend
#for now,I would post the plots of numerical factors in the plot folder


#create dummy for gender
#df["gender"]=df["gender"].fillna("Not Specified")
#dummiesgender = pd.get_dummies(df['gender']).rename(columns=lambda x: 'gender_' + str(x))
#df = pd.concat([df, dummiesgender], axis=1)
#df = df.drop(['gender'], inplace=True, axis=1)





