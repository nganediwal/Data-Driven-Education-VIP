# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 09:51:44 2020

@author: rache
"""

import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

df = pd.read_csv("./data/course_data.csv")
      
print(df.isnull().sum().sort_values(ascending=False))

#drop English col
df.drop(columns=['English'], inplace=True)


#fill null in education and gender with unspecified
df['level_of_education'].fillna('not specified', inplace=True)
df['gender'].fillna('not specified', inplace=True)

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