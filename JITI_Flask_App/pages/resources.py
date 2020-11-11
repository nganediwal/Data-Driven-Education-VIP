import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from globalvars import CONTENT_STYLE

# This is the resources page (currently has tutoring, teacher directory, and advising).
# TODO: Update with more resources as they come
# TODO: Decide what we want to do with the information that we get for each student (emailing them, etc)

page_layout = html.Div([
    html.Div(
        html.H1(
            "Welcome to your resources. Feel free to reach out and look for help!"
        ),  

        style = CONTENT_STYLE,
    ),

    dbc.Row(children = [
        
        dbc.Col(children = [
            dbc.Row(
                html.Img(src='/assets/tutoring.png', 
                    style = {
                        'max-height': '200px',
                        'margin' : 'auto',
                        'margin-bottom': '25px'
                    }
                ),
            ),

            dbc.Row(
                html.A(html.Button('Tutoring'), 
                href = 'http://success.gatech.edu/tutoring-0',
                style = {
                    'margin' : 'auto',
                }),
             ),
        ], 
            width={"size": 3, "offset" : 1},
        ),
        dbc.Col(children = [
            dbc.Row(
                html.Img(src='/assets/gtlogo.jpg', 
                    style = {
                        'max-height': '200px',
                        'margin' : 'auto',
                        'margin-bottom': '25px'
                    }
                ),
            ),

            dbc.Row(
                html.A(html.Button('Professor Directory'), 
                href = 'https://www.gatech.edu/offices-and-departments/',
                style = {
                    'margin' : 'auto',
                }),
             ),
        ], width={"size": 3}),

        dbc.Col(children = [
            dbc.Row(
                html.Img(src='/assets/advisor.png', 
                    style = {
                        'max-height': '200px',
                        'margin' : 'auto',
                        'margin-bottom': '25px'
                    }
                ),
            ),

            dbc.Row(
                html.A(html.Button('Advisor'), href = 'https://advisor.gatech.edu/',
                style = {
                    'margin' : 'auto',
                }),
             ),
        ], width={"size": 3},),
        

    ], align = "center", justify = "around"),

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