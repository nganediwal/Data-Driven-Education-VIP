import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from globalvars import CONTENT_STYLE

page_layout = html.Div([
    html.Div(
        html.H1(
            "Welcome to our displays of graphs and plots from our data modeling team!"
        ),  

        style = CONTENT_STYLE,
    ),

    dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/best_features.png', 
                style = {
                    'max-height': '1000px',
                    'margin' : 'auto',
                    'display' : 'block'
                }
            ),),
            html.Br(),
            dbc.Row(html.Button('best features',
                            style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
            )]),

    dcc.Link(html.Button('Home Page'), href = '/',
        style = {
            'margin' : 'auto',
            'position' : 'fixed',
            'bottom' : '10px',
            'left' : '10px',
        }
    ),
    dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/correlation.png', 
                style = {
                    'max-height': '2000px',
                    'margin' : 'auto',
                    'display' : 'block'
                }
            ),),
            html.Br(),
            dbc.Row(html.Button('Correlation',
                            style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
            )]),

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