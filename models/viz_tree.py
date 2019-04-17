from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
import graphviz
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
import os

grade_cutoff = 0.81

def getseconds(s):
    if s == 0:
    	return 0
    separated = s.split(" ")
    accumulator = 0
    if len(separated) == 3:
        accumulator += ((int)(separated[0])) * 24 * 60 * 60
    second_separated = separated[-1].split(":")
    accumulator += (int)(second_separated[0]) * 60 * 60
    accumulator += (int)(second_separated[1]) * 60
    accumulator += (int)(second_separated[2])
    return accumulator

def main():
    if len(sys.argv) < 2:
        print("Usage: python viz_tree.py <.csv file>")
        return 0

    df = pd.read_csv(sys.argv[1])
    df = df.fillna(0)

    df = df.drop(columns=["passed", 'user_id', 'course_id'])
    X = df.drop(columns=['percent_grade'])
    y = df['percent_grade'] > grade_cutoff

    X['time_diff'] = X['time_diff'].apply(getseconds)

    # print(X['time_diff'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestClassifier(n_estimators = 100, criterion = 'entropy', max_features = 'log2')

    rf.fit(X_train, y_train)

    estimator = rf.estimators_[50]

    print(len(rf.estimators_))

    dot_data = export_graphviz(estimator, 
                feature_names=X.columns,
                filled=True,
                rounded=True)
    os.system('dot -Tpng tree.dot -o tree.png')
    # from subprocess import call
    # call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])

main()