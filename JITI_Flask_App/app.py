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

# Set pandas display limit
pd.options.display.max_rows =999
pd.options.display.max_columns =999

print(dcc.__version__) # 0.6.0 or above is required

#get column names from studentdata.py
COLUMNNAMES = studentdata.COLUMNNAMES

# Need custom style sheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

######## PANDAS TEST DATA BELOW #############
test_df = data.testModelDF
student_data = studentdata.export_data_to_df('dataframe')
student_data = student_data.drop(columns = ['id'])

model_theta = studentdata.dummy_model_postgres('dummy_weights.csv', 3013850, 'user_id', 'dataframe')
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

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "z-index" : '5',
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "z-index" : '2',
    "width" : '80%'
}

sidebar = html.Div(
    [
        html.H2("Navigation Hub", className = "display-4"),
        html.Hr(),
        html.P("Where do you want to go?", className = "lead"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href ="/", id = "/"),
                dbc.NavLink("Resources", href ="resources", id = "resources"),
                dbc.NavLink("Table-data", href ="table-data", id = "table-data"),
                dbc.NavLink("Progress Over Time", href ="progress-over-time", id = "progress-over-time"),
                dbc.NavLink("Plots", href = "plots", id = "Plots")
            ],
            vertical = True,
            pills=True,
        ),
    ],
    style = SIDEBAR_STYLE
)

app.layout = html.Div([
    # url bar
    dcc.Location(id = 'url', refresh = False),

    #renders sidebar
    sidebar,

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
], 
style = CONTENT_STYLE
)

# Generating data table 
# if negative param display all data (up to 10 rows)
# else display the one student's data
def generate_table(studentID = -1):
    data = student_data.loc[student_data['user_id'] == studentID]
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in COLUMNNAMES])
        ),
        html.Tbody([
            html.Tr([
                html.Td(data.loc[student_data['week'] == 1][col]) for col in student_data.columns
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
    style = CONTENT_STYLE
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
            model_theta = studentdata.dummy_model_postgres('dummy_weights.csv', student_id, 'user_id', 'dataframe')
            return("Your predicted grade is ", model_theta)
            #test = np.asarray(student_data.iloc[1])
            #print(test)
            #data = np.zeros(b)
            #for x in range(b):
            #    if type(test[x]) == str:
            #        data[x] = 0
            #    else:
            #        data[x] = test[x]

            #print(data)
            #data = np.dot(data, model_theta)
            #return "Your predicted grade is: {:.2f}".format(data)

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
        #print(model_theta.shape)
        #print(np.sum(model_theta))
        return ''
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
], 
style = CONTENT_STYLE)

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

page_4_layout = html.Div([
    html.Div(id='plotButtons', children = []),
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
            dbc.Row(html.Button('best features', id='btn1',
                            style={'display':'block',
                                   'width' : '50%', 
                                   'margin':'0 auto',
                                   'align':'center'})
            )],
        
        style = CONTENT_STYLE    
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
            dbc.Row(html.Button('Correlation', id='btn2',
                            style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
            )]),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/gender.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('gender', id='btn3', n_clicks=0,
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/gender_vs_hypertext_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('gender_vs_hypertext_agg_count', id='btn4',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/gender_vs_load_video_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('gender_vs_load_video_agg_count', id='btn5',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ])
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/gender_vs_next_selected_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('gender_vs_next_selected_agg_count', id='btn6',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/gender_vs_page_close_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('gender_vs_page_close_agg_count', id='btn7',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/gender_vs_percent_progress.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('gender_vs_percent_progress', id='btn8',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ])
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/gender_vs_problem_check_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('gender_vs_problem_check_agg_count', id='btn9',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/gender_vs_problem_graded_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('gender_vs_problem_graded_agg_count', id='btn10',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/level_of_education.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('level_of_education', id='btn11',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ])
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/level_of_education_vs_hypertext_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('level_of_education_vs_hypertext_agg_count', id='btn12',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/level_of_education_vs_load_video_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('level_of_education_vs_load_video_agg_count', id='btn13',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/level_of_education_vs_next_selected_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('level_of_education_vs_next_selected_agg_count', id='btn14',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ])
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/level_of_education_vs_page_close_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('level_of_education_vs_page_close_agg_count', id='btn15',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/level_of_education_vs_percent_progress.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('level_of_education_vs_percent_progress', id='btn16',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/level_of_education_vs_problem_check_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('level_of_education_vs_problem_check_agg_count', id='btn17',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ])
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/level_of_education_vs_problem_graded_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('level_of_education_vs_problem_graded_agg_count', id='btn18',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/percent_progress.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('percent_progress', id='btn19',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/US.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('US', id='btn20',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ])
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/US_vs_hypertext_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('US_vs_hypertext_agg_count',id='btn21',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/US_vs_load_video_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('US_vs_load_video_agg_count',id='btn22',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/US_vs_next_selected_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('US_vs_next_selected_agg_count', id='btn23',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ])
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/US_vs_page_close_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('US_vs_page_close_agg_count', id='btn24',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/US_vs_percent_progress.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('US_vs_percent_progress', id='btn25',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/US_vs_problem_check_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('US_vs_problem_check_agg_count', id='btn26',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ])
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/US_vs_problem_graded_agg_count.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('US_vs_problem_graded_agg_count', id='btn27',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/yob_after.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('yob_after', id='btn28',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/yob_before.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('yob_before', id='btn29',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ])
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/YOB_boxplot_after.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('YOB_boxplot_after', id='btn30',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/YOB_boxplot_before.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('YOB_boxplot_before', id='btn31',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        ]
        ),

], 
style = CONTENT_STYLE
)

@app.callback(Output('plotButtons', 'children'),
              [Input('btn1', 'n_clicks'),
               Input('btn2', 'n_clicks'),
               Input('btn3', 'n_clicks'),
               Input('btn4', 'n_clicks'),
               Input('btn5', 'n_clicks'),
               Input('btn6', 'n_clicks'),
               Input('btn7', 'n_clicks'),
               Input('btn8', 'n_clicks'),
               Input('btn9', 'n_clicks'),
               Input('btn10', 'n_clicks'),
               Input('btn11', 'n_clicks'),
               Input('btn12', 'n_clicks'),
               Input('btn13', 'n_clicks'),
               Input('btn14', 'n_clicks'),
               Input('btn15', 'n_clicks'),
               Input('btn16', 'n_clicks'),
               Input('btn17', 'n_clicks'),
               Input('btn18', 'n_clicks'),
               Input('btn19', 'n_clicks'),
               Input('btn20', 'n_clicks'),
               Input('btn21', 'n_clicks'),
               Input('btn22', 'n_clicks'),
               Input('btn23', 'n_clicks'),
               Input('btn24', 'n_clicks'),
               Input('btn25', 'n_clicks'),
               Input('btn26', 'n_clicks'),
               Input('btn27', 'n_clicks'),
               Input('btn28', 'n_clicks'),
               Input('btn29', 'n_clicks'),
               Input('btn30', 'n_clicks'),
               Input('btn31', 'n_clicks'),])
def displayImage(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, 
                 btn11, btn12, btn13, btn14, btn15, btn16, btn17, btn18, btn19,
                btn20, btn21, btn22, btn23, btn24, btn25, btn26, btn27, btn28, 
                btn29, btn30, btn31):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn1.n_clicks' == changed_id:
        return modal('/assets/plots/best_features.png')
    if 'btn2.n_clicks' == changed_id:
        return modal('/assets/plots/correlation.png')
    if 'btn3.n_clicks' == changed_id:
        return modal('/assets/plots/gender.png')
    if 'btn4.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_hypertext_agg_count.png')
    if 'btn5.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_load_video_agg_count.png')
    if 'btn6.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_next_selected_agg_count.png')
    if 'btn7.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_page_close_agg_count.png')
    if 'btn8.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_percent_progress.png')
    if 'btn9.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_problem_check_agg_count.png')
    if 'btn10.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_problem_graded_agg_count.png')
    if 'btn11.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education.png')
    if 'btn12.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_hypertext_agg_count.png')
    if 'btn13.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_load_video_agg_count.png')
    if 'btn14.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_next_selected_agg_count.png')
    if 'btn15.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_page_close_agg_count.png')
    if 'btn16.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_percent_progress.png')
    if 'btn17.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_problem_check_agg_count.png')
    if 'btn18.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_problem_graded_agg_count.png')
    if 'btn19.n_clicks' == changed_id:
        return modal('/assets/plots/percent_progress.png')
    if 'btn20.n_clicks' == changed_id:
        return modal('/assets/plots/US.png')
    if 'btn21.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_hypertext_agg_count.png')
    if 'btn22.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_load_video_agg_count.png')
    if 'btn23.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_next_selected_agg_count.png')
    if 'btn24.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_page_close_agg_count.png')
    if 'btn25.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_percent_progress.png')
    if 'btn26.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_problem_check_agg_count.png')
    if 'btn27.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_problem_graded_agg_count.png')
    if 'btn28.n_clicks' == changed_id:
        return modal('/assets/plots/yob_after.png')
    if 'btn29.n_clicks' == changed_id:
        return modal('/assets/plots/yob_before.png')
    if 'btn30.n_clicks' == changed_id:
        return modal('/assets/plots/YOB_boxplot_after.png')
    if 'btn31.n_clicks' == changed_id:
        return modal('/assets/plots/YOB_boxplot_before.png')

def modal(path):
    if (path == ''):
        return None
    return html.Dialog(
        children=[
            html.Img(src=path,
                style = {
                    'maxHeight': '1500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            ),
            html.Button('Close', id='modal-close-button',
                        style = {'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
        ],
        id='modal',
        className='modal',
        style={"display": "block",
               'overflow': 'scroll',
               'height': '1080px',
               'width' : '1920px%',},
    )

@app.callback(Output('modal', 'style'),
              [Input('modal-close-button', 'n_clicks')])
def close_modal(n):
    if (n is not None):
        return {'display' : 'none'}
    else:
        return {'display' : 'block',
                'overflow': 'scroll'}

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
    elif pathname == '/plots':
        return page_4_layout

if __name__ == '__main__':
    app.run_server(debug=True)
