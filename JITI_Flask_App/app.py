# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
import data

# test imports
import dash_bootstrap_components as dbc

print(dcc.__version__) # 0.6.0 or above is required

# Need custom style sheet
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

######## PANDAS TEST DATA BELOW #############
test_df = data.test_df
######## PANDAS TEST DATA ABOVE #############

# initializing the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dictionary
colors = {
    'background': '#111111', #black
    'text': '#7FDBFF'
}

app.layout = html.Div([
    # url bar
    dcc.Location(id = 'url', refresh = False),

    # renders page content
    html.Div(id = 'page-content'),
])

index_page = html.Div([
    html.Div(
        html.H1(
            "Welcome, Beta_Tester!"
        ),  
        style = {
            'margin-bottom' : '100px'
        }
    ),

    # Example
    # dbc.Row(
    #     [
    #         dbc.Col(html.Div("One of three columns")),
    #         dbc.Col(html.Div("One of three columns")),
    #         dbc.Col(html.Div("One of three columns")),
    #     ]
    # ),

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
])





# table data
page_1_layout = html.Div(
    [
    dcc.Link('Home', href='/'),
    html.H1('Strengths and Weaknesses'),
    html.Div(
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in test_df.columns],
            data=test_df.to_dict('records'),
            style_table = {'overflowX' : 'scoll'},
            style_cell={
                'height': '30',
                'width': '70px',
            }
        ),
        style = {
            'margin-left': '200px',
            'margin-right': '200px'
        }
    )
    
    ]
)

# Progress over time
page_2_layout = html.Div([
    dcc.Link('Home', href = '/'),
    html.H1('Progress Over Time'),
    dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    y = np.random.normal(95, 2, size = 10),
                    name='A student',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                ),
                dict(
                    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    y = np.random.normal(80, 10, size = 10),
                    name='You',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=dict(
                title='Progress Over Time',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30),
                xaxis_title = 'week',
                yaxis_title = 'grade'
            )
        ),
        style={'height': 300},
        id='my-graph'
    ),  
])

# Resources
page_3_layout = html.Div([
    dcc.Link('Home', href = '/'),
    html.H1('Resources'),
])

# Update the URL, needed to render different pages

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/':
        return index_page
    elif pathname == '/table-data':
        return page_1_layout
    elif pathname == '/progress-over-time':
        return page_2_layout
    elif pathname == '/resources':
        return page_3_layout
    # else : 404 PAGE (not implemented)

if __name__ == '__main__':
    app.run_server(debug=True)