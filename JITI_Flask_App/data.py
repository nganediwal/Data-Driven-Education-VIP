import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np

def labeler(x):
    """
    This is a docstring, it should describe what this function does.
    """
    if x >= .9:
        return 'A'
    elif (x < .9) and (x >= .8):
        return 'B'
    elif (x < .8) and (x >= .7):
        return 'C'
    elif (x < .7) and (x >= .6):
        return 'D'
    return 'F'

## Shawn's aggregation stuff BELOW
np.random.seed(110)
grades = np.random.normal(0.8, 0.2, size=10)
click_count = np.random.normal(20, 5, size = 10)
grades[grades > 1] = 1
course_id = [1, 1, 2, 2, 3, 3, 3, 3, 3, 3]
user_id = [1, 2, 1, 2, 1, 2, 3, 4, 5, 6]

df = pd.DataFrame({
    'grade': grades,
    'course_id': course_id,
    'user_id': user_id
})

df = df.set_index(['course_id', 'user_id'])
df['label'] = df.grade.apply(labeler)
agg_df = df.groupby('label')['grade'].mean()
agg_df.columns = ['average grade']
## Shawn's aggregation stuff ABOVE

### Dummy data for table page
## Need to get data into a dataframe to pass into dash
letter_grades = ['A', 'B', 'C']
grades = np.random.normal(80, 10, size = 3)
click_count = np.random.normal(2000, 100, size = 3)
view_count = np.random.normal(10, 3, size = 3)
homework_grades = [94, 87, 70]
daily_visits = [2.6, 3.3, 2.6]

df = pd.DataFrame({
    'Letter Grade': letter_grades,
    'Numerical Grade': grades,
    'Click Count' : click_count,
    'View Count' : view_count,
    'Homework Grade': homework_grades,
    'Daily Visits': daily_visits
})

testModelDF = df

# Dummy data for score prediction
model_theta = np.array([.5, .3/20, .1, 0, .1*30]).T
student_data = {}
student_predicted_grade = {}

student_data[2000] = np.array([93.1, 95, 2200, 10, 94, 3.2])
student_data[2001] = np.array([85, 87, 1933, 4, 84, 2.8])

letter_grades = ['A', 'B', 'C']
grades = [93.1, 85, 77]
click_count = [2200, 1933, 1600]
view_count = [10, 4, 1]
homework_grades = [94, 87, 70]
daily_visits = [3.2, 3.3, 2.6]

student_data = pd.DataFrame({
    'Letter Grade': letter_grades,
    'Numerical Grade': grades,
    'Click Count' : click_count,
    'View Count' : view_count,
    'Homework Grade': homework_grades,
    'Daily Visits': daily_visits
})

# test_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
