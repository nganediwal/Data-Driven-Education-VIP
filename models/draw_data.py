import plotly.plotly as py
import plotly.tools as tls

import matplotlib.pyplot as plt
import numpy as np

import sys
import csv

random_forest = []
gradient_boost = []
logistic_regression = []
SVM = []
Adaboost = []

with open(sys.argv[1]) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if row[2] == 'random_forest':
            random_forest += [float(row[0])]
        if row[2] == 'gradient_boost':
            gradient_boost += [float(row[0])]
        if row[2] == 'logistic_regression':
            logistic_regression += [float(row[0])]
        if row[2] == 'SVM':
            SVM += [float(row[0])]
        if row[2] == 'ADABoost':
            Adaboost += [float(row[0])]

data = [random_forest, gradient_boost, logistic_regression, SVM, Adaboost]

# print(data)

mpl_fig = plt.figure()
ax = mpl_fig.add_subplot(111)

labels = ['Random Forest', 'Gradient Boost', 'Logistic Regression', 'SVM', 'Adaboost']

ax.boxplot(data, labels=['Random Forest', 'Gradient Boost', 'Logistic Regression', 'SVM', 'Adaboost'])
ax.set_xticks(range(1,6))
ax.set_xticklabels(labels)
# plt.setp(xtickNames, rotation=45, fontsize=8)
ax.set_title("Performance of Models")

plotly_fig = tls.mpl_to_plotly( mpl_fig )
plotly_fig['layout']['xaxis1'].update({'ticktext': labels, 'tickvals': [1,2,3,4,5]})
py.iplot(plotly_fig, filename='mpl-multiple-boxplot')