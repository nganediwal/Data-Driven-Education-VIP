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
        html.Div(dcc.Input(id='student_id', type='number')),
        html.Div(dcc.Dropdown(
            id='student_course',
            options=[
                {'label': 'Management 1000 Completion', 'value': 'MGT1000 Completion'},
                {'label': 'Management 1000 Grade', 'value': 'MGT1000 Grade'},
                {'label': 'Computer Science 1301 Completion', 'value': 'CS1301 Completion'},
                {'label': 'Computer Science 1301 Grade', 'value': 'CS1301 Grade'},
            ],
            value='MGT1000 Completion'
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