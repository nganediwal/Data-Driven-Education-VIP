# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import numpy as np
import data
import studentdata
import plotly.graph_objs as go

# test imports
import dash_bootstrap_components as dbc

print(dcc.__version__) # 0.6.0 or above is required

#get column names from studentdata.py
COLUMNNAMES = studentdata.COLUMNNAMES

# Need custom style sheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

######## PANDAS TEST DATA BELOW #############
test_df = data.testModelDF
student_data = studentdata.export_data_to_df('info', 'id')
model_theta = data.model_theta
# print(student_predicted_grade)
######## PANDAS TEST DATA ABOVE #############

# initializing the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#To fix callback exceptions, need to include ids in the INITIAL state
app.config['suppress_callback_exceptions'] = True

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
])

# Generating data table 
# if negative param display all data (up to 10 rows)
# else display the one student's data
def generate_table(studentID = -1):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in COLUMNNAMES])
        ),
        html.Tbody([
            html.Tr([
                html.Td(student_data.iloc[studentID][col]) for col in student_data.columns
            ])
        ])
    ])

## TODO: Put all the attributes into a list, iterate through and display student values
## Basically, display their stats and make it look nicer

## TODO: Iterate through student attributes in callback, update the "weakness" message 
# depending on what's below average

# table data
page_1_layout = html.Div(
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

    # Take user input for prediction
    # displays current stats and not weaknesses (not implemented)

    html.Div([
        
        html.H1(
            "Enter ID"
        ),  
        html.Div([
        html.Div(dcc.Input(id='student_id', type='number'))
        ]),

        html.H1(id='predicted_score', 
             # Margin after the score

        ),
        html.H1(id='current_stats'),
        
        # For testing the new data and for when we get the actual data
        # testing output; comment out if not testing new data
        html.H1(id='data_testing'),

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
    style = {
        'margin-left': '100px',
    }
)

## STRENGTHS AND WEAKNESSES CALLBACKS for student ID
# Predicted Grade / Predicted Score
@app.callback(
    Output(component_id ='predicted_score', component_property='children'),
    [Input(component_id='student_id', component_property='value')]
)

# Fake model used to predict 3 students' scores 
# Those ID's can be 0, 1, 2 (respectively A, B, C students)
def update_predicted_score(student_id):
    try:

        if (student_id == None):
            return "Grade cannot be predicted with no ID"
            
        if(student_id < 0):
            return "id cannot be negative"

        else:
            test = student_data.to_numpy()[student_id, 1:]
            test = test.dot(model_theta)
            return "Your predicted grade is: {:.2f}".format(test)

    except:
        return "Grade cannot be predicted with invalid ID"

# Current stats 
# outputs table of selected student
# or if negative # outputs entire table
@app.callback(
    dash.dependencies.Output('current_stats', 'children'),
    [dash.dependencies.Input('student_id', 'value')]
)
def update_current_stats(value):
    try:
        if (value == None):
            return "stats cannot be shown with no ID"

        if (value < 0):
            return generate_table(-1)

        else:
            return generate_table(int(value))

    except:
        return "Grade cannot be shown with invalid ID"
        
#for testing data. Can comment out when not testing with new data inputs.
@app.callback(
    dash.dependencies.Output('data_testing', 'children'),
    [dash.dependencies.Input('student_id', 'value')]
)
def update_current_stats(value):
    try:
        #print(studentdata.get_student_data_PSQL(35087))
        #print(studentdata.get_student_data_mongoDB(58294))
        #print(COLUMNNAMES)
        #x =  (studentdata.export_data_to_df('info', 'id'))
        #list = x.values.tolist()[0]
        #print(list)
        #string = "\n".join([str(elem) for elem in list])
        #student_data = x
        #return string
        return ""
    except:
        return "Error has occurred with data testing"

# Progress over time
# Updated: dropdown menu, callback, and average A, B, C student grade, view counts
# Updated: x-axis and y-axis title on the layout
# Error: The code runs perfectly and gives right graph but shows a error on the webpage 'ID not found in layout'
# Please check it out

page_2_layout = html.Div([
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
])

#The function will create graphs based on the factors in the dropdown menu
#Each Graph contains 4 sets of data that can show the average for A, B, C students, and individual student's record

def plot_summary(option= None):

    #set common variables
    index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ColorA = dict(color='rgb(249, 197, 5)')
    ColorB = dict(color='rgb(220, 104, 34)')
    ColorC = dict(color='rgb(45, 133, 116)')
    ColorU = dict(color='rgb(26, 118, 255)')
    Layout_legend= dict(x=0,y=1.0)
    Layout_margin = dict(l=40, r=0, t=40, b=30)
   
    #Graph for Numberical Grade
    if option == 'Numerical Grade':
        figure=dict(
            data=[
                dict(
                    x = index,
                    y = np.random.normal(95, 2, size = 10),
                    name='A',
                    marker= ColorA
                ),
                dict(
                    x = index,
                    y = np.random.normal(85, 2, size = 10),
                    name='B',
                    marker= ColorB
                ), 
                dict(
                    x = index,
                    y = np.random.normal(75, 2, size = 10),
                    name='C',
                    marker= ColorC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
                ),
                dict(
                    x = index,
                    y = np.random.normal(80, 2, size = 10),
                    name='Your Grade',
                    marker= ColorU
                )
            ],
            layout=dict(
                title = 'Numerical Grades Over Time',
                showlegend=True,
                legend=Layout_legend,
                margin=Layout_margin,
                xaxis=dict(title='Week'),
                yaxis=dict(title='Grade')
            ),
            
        )
    # Graph for student view counts
    elif option == 'View Counts':
        figure=dict(
            data=[
                dict(
                    x = index,
                    y = np.random.normal(10, 1, size = 10),
                    name='A Views',
                    marker=ColorA
                ),
                dict(
                    x = index,
                    y = np.random.normal(8, 1, size = 10),
                    name='B Views',
                    marker=ColorB
                ),
                dict(
                    x = index,
                    y = np.random.normal(5, 1, size = 10),
                    name='C Views',
                    marker=ColorC
                ),
                dict(
                    x = index,
                    y = np.random.normal(7, 1, size = 10),
                    name='Your Views',
                    marker=ColorU
                )
            ],
            layout=dict(title = "View Counts Over Time",
                showlegend=True,
                legend=Layout_legend,
                margin=Layout_margin,
                yaxis=dict(title='View Counts')
            )
        )
    #Graph for student click counts
    elif option == 'Click Counts':
        figure=dict(
            data=[
                dict(
                    x = index,
                    y = np.random.normal(3000, 100, size = 10),
                    name='A Clicks',
                    marker=ColorA
                ),
                dict(
                    x = index,
                    y = np.random.normal(2000, 100, size = 10),
                    name='B Clicks',
                    marker=ColorB
                ),
                dict(
                    x = index,
                    y = np.random.normal(1000, 100, size = 10),
                    name='C Clicks',
                    marker=ColorC
                ),
                dict(
                    x = index,
                    y = np.random.normal(1952, 100, size = 10),
                    name='Your Clicks',
                    marker=ColorU
                )
            ],
            layout=dict(title = "Click Counts Over Time",
                showlegend=True,
                legend=Layout_legend,
                margin=Layout_margin,
                yaxis=dict(title='Click Counts')
            )
        )
    # Graph for student homework grade
    elif option == 'Homework Grade':
        figure=dict(
            data=[
                dict(
                    x = index,
                    y = np.random.normal(92, 2, size = 10),
                    name='A',
                    marker=ColorA
                ),
                dict(
                    x = index,
                    y = np.random.normal(85, 2, size = 10),
                    name='B',
                    marker=ColorB
                ),
                dict(
                    x = index,
                    y = np.random.normal(75, 2, size = 10),
                    name='C',
                    marker=ColorC
                ),
                dict(
                    x = index,
                    y = np.random.normal(80, 2, size = 10),
                    name='Your Grade',
                    marker=ColorU
                )
            ],
            layout=dict(title = "Homework Grades Over Time",
                showlegend=True,
                legend=Layout_legend,
                margin=Layout_margin,
                xaxis=dict(title='Week'),
                yaxis=dict(title='View Counts')
            )
        )
    #Graph for student daily visits
    else:
        figure=dict(
            data=[
                dict(
                    x = index,
                    y = np.random.normal(4, 0.5, size = 10),
                    name='A daily visits',
                    marker=ColorA
                ),
                dict(
                    x = index,
                    y = np.random.normal(3, 0.3, size = 10),
                    name='B daily visits',
                    marker=ColorB
                ),
                dict(
                    x = index,
                    y = np.random.normal(2, 0.4, size = 10),
                    name='C daily visits',
                    marker=ColorC
                ),
                dict(
                    x = index,
                    y = np.random.normal(3, 0.2, size = 10),
                    name='Your daily visits',
                    marker=ColorU
                )
            ],
            layout=dict(title = "Daily Visits Over Time",
                showlegend=True,
                legend=Layout_legend,
                margin=Layout_margin,
                xaxis=dict(title='Week'),
                yaxis=dict(title='Daily Visits')
            )
        )
    
    return (figure)


#page_2_callback

@app.callback(Output('feature-graphic', 'figure'),
             [Input('yaxis', 'value') ] )

#recall the function above
def make_graph(page_2_dropdown):
    fig = plot_summary(option = page_2_dropdown)
    return fig


# Resources
page_3_layout = html.Div([
    html.Div(
        html.H1(
            "Welcome to your resources. Feel free to reach out and look for help!"
        ),  

        style = {
            'margin-bottom' : '100px',
        }
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

if __name__ == '__main__':
    app.run_server(debug=True)
