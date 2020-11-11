import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_excel
import seaborn as sns
from scipy import stats

#create dummy, outlier removal and prepare for further analysis

df = pd.read_excel('MOOC_course data VIP-V2.xlsx', sep=',')
#df = df.set_index('percent_progress')
#ata = [df["gender"],df["level_of_education"]]
#eaders = ['gender',"level_of_education"]
#f1 = pd.concat(data, axis=1, keys=headers)
del df['US']
del df["English"]
df["level_of_education"]=df["level_of_education"].fillna("Not Specified")
df["gender"]=df["gender"].fillna("Not Specified")
df = df.dropna(axis=0)
dummiesgender = pd.get_dummies(df['gender']).rename(columns=lambda x: 'gender_' + str(x))
dummieseducation = pd.get_dummies(df['level_of_education']).rename(columns=lambda x: 'edu_' + str(x))
df = pd.concat([df, dummieseducation], axis=1)
df = pd.concat([df, dummiesgender], axis=1)
df['Age'] = pd.datetime.now().year - df.year_of_birth
del df["gender"]
del df["level_of_education"]
del df["year_of_birth"]
z_scores = stats.zscore(df)
abs_z_scores = np.abs(z_scores)
filtered_entries = (abs_z_scores < 2).all(axis=1)
filtered_df = df[filtered_entries]
filtered_df





