# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
import data
import plotly.graph_objs as go

# test imports
import dash_bootstrap_components as dbc

print(dcc.__version__) # 0.6.0 or above is required

# Need custom style sheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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

app.config['suppress_callback_exceptions'] = True

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
            # Maybe change to scroll
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
# Updated: dropdown menu, callback, and average A, B, C student grade, view counts
# Updated: x-axis and y-axis title on the layout
# Error: The code runs perfectly and gives right graph but shows a error on the webpage 'ID not found in layout'
# Please check it out

page_2_layout = html.Div([
    dcc.Link('Home', href = '/'),
    html.H1('Progress Over Time'),
    dcc.Dropdown(
        id='page_2_dropdown',
        options=[
            {'label': 'Numerical Grade', 'value': 'Numerical Grade'},
            {'label': 'View Counts', 'value': 'View Counts'}
        ],
        value='Numerical_grade'
    ),
    dcc.Graph(id = 'page_2_graph',
            style={'height': 300})
])

def plot_summary(option= None):
    if option == 'Numerical Grade':
        figure=dict(
            data=[
                dict(
                    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    y = np.random.normal(95, 2, size = 10),
                    name='A',
                    marker=dict(
                        color='rgb(249, 197, 5)'
                    )
                ),
                dict(
                    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    y = np.random.normal(85, 2, size = 10),
                    name='B',
                    marker=dict(
                        color='rgb(220, 104, 34)'
                    )
                ),
                dict(
                    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    y = np.random.normal(75, 2, size = 10),
                    name='C',
                    marker=dict(
                        color='rgb(45, 133, 116)'
                    )
                ),
                dict(
                    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    y = np.random.normal(80, 5, size = 10),
                    name='You',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=dict(
                title = 'Numerical Grade',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30),
                xaxis=dict(title='Week'),
                yaxis=dict(title='Grade')
            ),
            
        )
    else:
        figure=dict(
            data=[
                dict(
                    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    y = np.random.normal(8, 2, size = 10),
                    name='A Student',
                    marker=dict(
                        color='rgb(249, 197, 5)'
                    )
                ),
                dict(
                    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    y = np.random.normal(6, 2, size = 10),
                    name='B Student',
                    marker=dict(
                        color='rgb(220, 104, 34)'
                    )
                ),
                dict(
                    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    y = np.random.normal(3, 2, size = 10),
                    name='C Student',
                    marker=dict(
                        color='rgb(45, 133, 116)'
                    )
                ),
                dict(
                    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    y = np.random.normal(5, 2, size = 10),
                    name='You',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=dict(title = "View Counts",
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30),
                xaxis=dict(title='Week'),
                yaxis=dict(title='View Counts')
            )
        )
    return (figure)

#page_2_callback

@app.callback(
    dash.dependencies.Output('page_2_graph', 'figure'),
    [dash.dependencies.Input('page_2_dropdown', 'value') ] )

def make_graph(page_2_dropdown):
    fig = plot_summary(option = page_2_dropdown)
    return fig


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