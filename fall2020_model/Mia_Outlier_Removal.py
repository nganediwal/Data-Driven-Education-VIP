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


# previous code with outlier table creation and plots



  df = df.set_index('percent_progress')
  del df['English']
  del df['US']
  del df['Age']
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






