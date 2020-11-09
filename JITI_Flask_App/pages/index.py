import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output


from globalvars import CONTENT_STYLE

page_layout = html.Div([
    html.Div(
        html.H1(
            "Welcome, Beta_Tester!"
        ),  

        style = {
            'margin-bottom' : '100px',
        }
    ),

    dbc.Row(children = [
        
        dbc.Col(children = [
            dbc.Row(
                html.Img(src='/assets/strengths-and-weaknesses.jpg', 
                    style = {
                        'max-height': '200px',
                        'margin' : 'auto',
                        'margin-bottom': '25px'
                    }
                ),
            ),

            dbc.Row(
                dcc.Link(html.Button('Strengths and Weaknesses'), href = '/table-data',
                    style = {
                        'margin' : 'auto',
                    }
                ),
            ),
        ], 
            width={"size": 3, "offset" : 1},
        ),
        dbc.Col(children = [
            dbc.Row(
                html.Img(src='/assets/clock.jpg', 
                    style = {
                        'max-height': '200px',
                        'margin' : 'auto',
                        'margin-bottom': '25px'
                    }
                ),
            ),

            dbc.Row(
                dcc.Link(html.Button('Progress Over Time'), href = '/progress-over-time',
                    style = {
                        'margin' : 'auto',
                    }
                ),
            ),
        ], width={"size": 3}),

        dbc.Col(children = [
            dbc.Row(
                html.Img(src='/assets/books.jpg', 
                    style = {
                        'max-height': '200px',
                        'margin' : 'auto',
                        'margin-bottom': '25px'
                    }
                ),
            ),

            dbc.Row(
                dcc.Link(html.Button('Resources'), href = '/resources',
                style = {
                    'margin' : 'auto',
                }),
            ),
        ], width={"size": 3},),
        

    ], align = "center", justify = "around"),
], 
style = CONTENT_STYLE
)