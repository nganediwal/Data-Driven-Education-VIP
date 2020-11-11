import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

import data
import studentdata

# initializing the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#To fix callback exceptions, need to include ids in the INITIAL state
app.config['suppress_callback_exceptions'] = True

# Set pandas display limit
pd.options.display.max_rows =999
pd.options.display.max_columns =999

#get column names from studentdata.py
COLUMNNAMES = studentdata.COLUMNNAMES

# Need custom style sheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

######## PANDAS TEST DATA BELOW #############
test_df = data.testModelDF
student_data = studentdata.export_data_to_df('dataframe')
student_data = student_data.drop(columns = ['id'])

model_theta = studentdata.dummy_model_postgres('dummy_weights.csv', 3013850, 'user_id', 'dataframe')
# print(student_predicted_grade)
######## PANDAS TEST DATA ABOVE #############

# Dictionary
colors = {
    'background': '#111111', #black
    'text': '#7FDBFF'
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}