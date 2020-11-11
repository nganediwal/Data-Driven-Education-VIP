import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from globalvars import test_df, CONTENT_STYLE, app

# Page for 2020 FALL modeling team's model for % completion. 
# takes input student ID and outputs predicted % completion.

page_layout = html.Div([
        
        html.H1(
            "Enter ID",
        ),  
        html.Div([
        html.Div(dcc.Input(id='student_id', type='number'))
        ]),

        html.H1(id='predicted_completion', 

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