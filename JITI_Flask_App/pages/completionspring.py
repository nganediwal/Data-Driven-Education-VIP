import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from globalvars import test_df, CONTENT_STYLE, app

page_layout = html.Div([
        
        html.H1(
            "Enter ID",
        ),  
        html.Div([
        html.Div(dcc.Input(id='student_id', type='number', placeholder="Student ID", debounce=True)),
        html.Div(dcc.Input(id='week', type='number', placeholder="Week", debounce=True)),
        html.Div(dcc.Dropdown(
            id='student_course',
            options=[
                {'label': 'Management 100 Normal', 'value': 'MGT100N'},
                {'label': 'Management 100 Timeseries', 'value': 'MGT100TS'},
                {'label': 'Computer Science 1301 Normal', 'value': 'CS1301N'},
                {'label': 'Computer Science 1301 Timeseries', 'value': 'CS1301TS'},
            ],
            value='MGT100N'
        )),
        ]),


        html.H1(id='predicted_completion_spring21', 

        ),

    dcc.Link(html.Button('Home Page'), href = '/',
        style = {
            'margin' : 'auto',
            'position' : 'fixed',
            'bottom' : '10px',
            'left' : '10px',
        }
    )
    ],
    style = CONTENT_STYLE
)