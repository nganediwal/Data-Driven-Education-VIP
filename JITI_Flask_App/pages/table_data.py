import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from globalvars import test_df, CONTENT_STYLE, app

# Page for displaying table data of each student.
# The model is currently a fake one and we do not have access to something better.

page_layout = html.Div(
    [
    html.H1('Strengths and Weaknesses'),

    html.Div(
        dash_table.DataTable(
            id='table',
            # Allows us to delete columns
            columns=[{"name": i, "id": i, "deletable": True} for i in test_df.columns],
            data=test_df.to_dict('records'),
            # Allows us to filter rows
            filter_action="native",
            style_table = {'overflowX' : 'scoll'},
            style_cell={
                'height': '30',
                'width': '70px',
            }
        ),
        style = {
            'margin-left': '200px',
            'margin-right': '200px',
            'margin-bottom': '25px',
            'margin-top': '25px'
        }
    ),

    html.Div([
        
        html.H1(
            "Enter ID",
        ),  
        html.Div([
        html.Div(dcc.Input(id='student_id', type='number'))
        ]),

        html.H1(id='predicted_score', 

        ),
        html.H1(id='current_stats',
            style = {
                'font-size': '25px',
                'overflow': 'scroll',
            }
            ),
    ]),

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