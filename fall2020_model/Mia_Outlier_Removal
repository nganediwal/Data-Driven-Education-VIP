import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_excel
import seaborn as sns
from scipy import stats

df = pd.read_excel('MOOC_course data VIP-V2.xlsx', sep=',')
del df['English']
del df['US']
df["level_of_education"]=df["level_of_education"].fillna("Not Specified")


# Temp drop all na value
df = df.dropna(axis=0)

#plot indivisual variable to obsere outlier
sns.boxplot(df["year_of_birth"])


# Create z-score columns of all numerical variables
df2 = df

z_column = list(df.columns)
z_column .remove('gender')
z_column .remove('level_of_education')
df2[z_column]

for col in z_column:
    col_zscore = col + '_zscore'
    df2[col_zscore] = (df2[col] - df2[col].mean())/df2[col].std(ddof=0)
    
#drop rows with z-score higher than 3 or lower than -3

for col in z_cols:
    df2.drop(df2[df2[col] < -3].index, inplace = True)
    df2.drop(df2[df2[col] > 3].index, inplace = True) 


#plot numerical variable to see if we seccefully removed outliers
sns.boxplot(df2["year_of_birth"])

#create dummy for gender

df["gender"]=df["gender"].fillna("Not Specified")
dummiesgender = pd.get_dummies(df['gender']).rename(columns=lambda x: 'gender_' + str(x))
df = pd.concat([df, dummiesgender], axis=1)
#df = df.drop(['gender'], inplace=True, axis=1)


