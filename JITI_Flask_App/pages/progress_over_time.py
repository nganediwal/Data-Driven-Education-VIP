import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from globalvars import CONTENT_STYLE

# Progress over time
# Updated: dropdown menu, callback, and average A, B, C student grade, view counts
# Updated: x-axis and y-axis title on the layout
# Error: The code runs perfectly and gives right graph but shows a error on the webpage 'ID not found in layout'
# Please check it out

page_layout = html.Div([
    html.H1('Progress Over Time'),
    
    #Dropdown menu for different graphs
    dcc.Dropdown(
        id='yaxis',#set id enable call back
        options=[
            {'label': 'Numerical Grade', 'value': 'Numerical Grade'},
            {'label': 'View Counts', 'value': 'View Counts'},
            {'label': 'Click Counts', 'value': 'Click Counts'},
            {'label': 'Homework Grade', 'value': 'Homework Grade'},
            {'label': 'Daily Visits', 'value': 'Daily Visits'}
        ],
        value='Numerical_grade'#set initial value
    ),

    dcc.Graph(id = 'feature-graphic',
            style={'height': 500}),

    dcc.Link(html.Button('Home Page'), href = '/',
        style = {
            'margin' : 'auto',
            'position' : 'fixed',
            'bottom' : '10px',
            'left' : '10px',
        }
    )
], 
style = CONTENT_STYLE)