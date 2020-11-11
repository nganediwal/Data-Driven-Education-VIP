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
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/outlier/num_of_outlier.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('num_of_outlier', id='btn32',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/gender/gender_education_not_spec.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('gender_education_not_spec', id='btn33',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/gender/gender_ percent_progress.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('gender_ percent_progress', id='btn34',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/education/education_percent_progress.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('education_percent_progress', id='btn35',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/education/education_level.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'height' : '500px',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('education_level', id='btn36',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/education/age_vs_not_specified_gender_and_education.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('age_vs_not_specified_gender_and_education', id='btn37',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/education/age_level_of_education.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('age_level_of_education', id='btn38',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/behavior/stop_vs_next_on_pause.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('stop_vs_next_on_pause', id='btn39',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/behavior/Speed_change_vs_percent_progress.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('Speed_change_vs_percent_progress', id='btn40',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/behavior/prev_vs_next_vs_percent progress1.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('prev_vs_next_vs_percent progress1', id='btn41',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/behavior/pause_on_load.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('pause_on_load', id='btn42',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/behavior/next_pause_vs_gender_and_education_level.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('next_pause_vs_gender_and_education_level', id='btn43',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/behavior/next_n_prev_vs_progress_regression1.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('next_n_prev_vs_progress_regression1', id='btn44',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        ]
        ),
    dbc.Row(children = [
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/behavior/next_n_prev_vs_progress_regression.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('next_n_prev_vs_progress_regression', id='btn45',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/age/Age_outlier_vs_percent_progress.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('Age_outlier_vs_percent_progress', id='btn46',
                           style={'display':'block',
                                   'width' : '400px', 
                                   'margin':'0 auto',
                                   'align':'center'})
                )
            ]),
        dbc.Col(children = [
            dbc.Row(html.Img(src='/assets/plots/plots/age/Age_distribution_vs_percent_Progress.png',
                style = {
                    'max-height': '500px',
                    'margin': 'auto',
                    'display':'block'
                    }
            )),
            dbc.Row(html.Button('Age_distribution_vs_percent_Progress', id='btn47',
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