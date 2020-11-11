import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from globalvars import CONTENT_STYLE

# Plots page from the modeling team.
# Displaying the plots from the modeling team and allowing for close-up views through a modal.
# TODO: The images aren't on their own blocks / can cover one another.
#   *We need to work on getting this page to be responsive to monitor widths and sizes.

page_layout = html.Div([
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
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
            )]),

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