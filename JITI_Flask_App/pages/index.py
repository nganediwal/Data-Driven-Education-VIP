import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output

from globalvars import CONTENT_STYLE


table_data = [
    dbc.CardHeader("Table Data Page"),
    dbc.CardBody(
        [
            # html.H5("Table-data Page", className="card-title"),
            html.P(
                "Table data page provides information on .......",
                className="card-text",
            ),
            dbc.Button(
                "View Page", size="lg", color="success", className="mr-1",
                href='table-data',
            ),
        ]

    ),
]

progress_over_time = [
    dbc.CardHeader("Progress Over Time Page"),
    dbc.CardBody(
        [
            # html.H5("Table-data Page", className="card-title"),
            html.P(
                "Progress Over Time Page provides information on .......",
                className="card-text",
            ),
            dbc.Button(
                "View Page", size="lg", color="success", className="mr-1",
                href='progress-over-time',
            ),
        ]

    ),
]

plots = [
    dbc.CardHeader("Plots"),
    dbc.CardBody(
        [
            # html.H5("Table-data Page", className="card-title"),
            html.P(
                "The Plots page displays ........",
                className="card-text",
            ),
            dbc.Button(
                    "View Page",size="lg",color="success", className="mr-1",
                    href='plots',
            ),
        ]
    ),
]
completion_prediction = [
    dbc.CardHeader("Completion Prediction Page"),
    dbc.CardBody(
        [
            # html.H5("Table-data Page", className="card-title"),
            html.P(
                "Completion Prediction Page displays .......",
                className="card-text",
            ),
            dbc.Button(
                    "View Page",size="lg",color="success", className="mr-1",
                    href='completion',

            ),
        ]

    ),
]


page_layout = html.Div([

    html.Div(
        html.H1(
            "Just In Time Intervention (JITI)"
        ),

        style = {
            'margin-top' : '30px','margin-bottom' : '10px','text-align': 'center',
        }
    ),

    html.Div(
        html.H6(
            "Created by: Data-Driven Education - JITI sub-team"
        ),

        style = {
            'margin-top' : '10px','margin-bottom' : '10px','text-align': 'center','font-style': 'italic',
        }
    ),

    html.Div(
        html.P(
            "Welcome to the Just-In-Time Intervention web app! The purpose of this website is to use data-driven "
            "techniques such as machine learning and statistical analysis to provide you (the student) with tools "
            "that can help you succeed in your classes."
        ),

        style = {
            'margin-top' : '60px','margin-bottom' : '30px','text-align': 'center','font-size': '19px'
        }
    ),

    html.Div(
        dbc.Card(
        dbc.CardBody(
            [
                html.H5("View the Prediction Page", className="card-title"),
                # html.P(
                #     "This card also has some text content and not much else, but "
                #     "it is twice as wide as the first card."
                # ),
                dbc.Button("View App", color="success",size="lg",
                           href='completion',),
            ]
        ),
        ),
        style={'margin-left' : 'auto','margin-right' : 'auto','text-align': 'center','font-size': '30px'},
    ),



    html.Div(

        style = {
            'margin-top' : '40px',
        }
    ),

    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card(table_data, color="dark", inverse=True)),
                    dbc.Col(dbc.Card(progress_over_time, color="dark", inverse=True)),
                ]
            ),

        ]
    ),

    html.Div(

        style = {
            'margin-top' : '20px',
        }
    ),

    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card(plots, color="dark", inverse=True)),
                    dbc.Col(dbc.Card(completion_prediction, color="dark", inverse=True)),
                ]
            ),
            # dbc.(style={"margin-top": "20"})
        ]
    ),
],
style = CONTENT_STYLE,
)
