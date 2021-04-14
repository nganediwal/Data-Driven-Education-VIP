# -*- coding: utf-8 -*-
import os
from pages import index, plots, progress_over_time, resources, table_data, completion, completionspring
from globalvars import *

print(dcc.__version__) # 0.6.0 or above is required

# Main python file with callbacks for the Dash app.

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#sidebar of the whole app
#if adding a new link/page, add a dbc.NavLink like shown
sidebar = html.Div(
    [
        html.H2("JITI Web App", className = "display-4"),
        html.Hr(),
        html.P("Where do you want to go?", className = "lead"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href ="/", id = "/"),
                dbc.NavLink("Resources", href ="resources", id = "resources"),
                dbc.NavLink("Table-data", href ="table-data", id = "table-data"),
                dbc.NavLink("Progress Over Time", href ="progress-over-time", id = "progress-over-time"),
                dbc.NavLink("Plots", href = "plots", id = "Plots"),
                dbc.NavLink("Completion Prediction", href = "completion", id = "completion"),
                dbc.NavLink("Spring Models", href = "completionspring", id = "completionspring"),
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



# Generating data table 
# if negative param display empty table
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



# Current stats 
# outputs table of selected student
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

# STRENGTHS AND WEAKNESSES CALLBACKS for student ID
# Predicted Grade / Predicted Score
@app.callback(
    Output(component_id ='predicted_score', component_property='children'),
    [Input(component_id='student_id', component_property='value')]
)

def update_predicted_score(student_id):
    try:

        if (student_id == None):
            return "Grade cannot be predicted with no ID"
            
        if(student_id < 0):
            return "id cannot be negative"

        else:
            model_theta = studentdata.dummy_model_postgres('dummy_weights.csv', student_id, 'user_id', 'dataframe')
            return("Your predicted grade is ", model_theta)

    except:
        return "Grade cannot be predicted with invalid ID"

# Predicted Grade / Predicted Score
@app.callback(
    Output(component_id ='predicted_completion_spring21', component_property='children'),
    [Input(component_id='student_id', component_property='value'), Input(component_id='student_course', component_property='value')]
)

def update_predicted_score_spring21(student_id, student_course):
    try:

        if (student_id == None):
            return "Completion cannot be predicted with no ID"
            
        if(student_id < 0):
            return "id cannot be negative"

        else:
            model_theta = studentdata.predict_completion(student_id) * 100
            return("Your predicted completion is ", model_theta, "%  ", student_course)

    except:
        return "Completion cannot be predicted with invalid ID"
    
@app.callback(
    Output(component_id ='predicted_completion', component_property='children'),
    [Input(component_id='student_id', component_property='value')]
)

# Used in completion.py
# predicts completion %
# Aashay, replace the function dummy_model_postgrest() with the one you added to studentdata

def update_predicted_completion(student_id):
    try:

        if (student_id == None):
            return "Completion cannot be predicted with no ID"
            
        if(student_id < 0):
            return "id cannot be negative"

        else:
            model_theta = studentdata.predict_completion(student_id) * 100
            return("Your predicted completion is ", model_theta, "%")

    except:
        return "Completion cannot be predicted with invalid ID"

# The function will create graphs based on the factors in the dropdown menu
# Each Graph contains 4 sets of data that can show the average for A, B, C students, and individual student's record

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

@app.callback(Output('feature-graphic', 'figure'),
             [Input('yaxis', 'value') ] )

def make_graph(page_2_dropdown):
    fig = plot_summary(option = page_2_dropdown)
    return fig

# Callback for Plots page
# Really messy needed the input of 31 buttons.

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
               Input('btn31', 'n_clicks'),
               Input('btn32', 'n_clicks'),
               Input('btn33', 'n_clicks'),
               Input('btn34', 'n_clicks'),
               Input('btn35', 'n_clicks'),
               Input('btn36', 'n_clicks'),
               Input('btn37', 'n_clicks'),
               Input('btn38', 'n_clicks'),
               Input('btn39', 'n_clicks'),
               Input('btn40', 'n_clicks'),
               Input('btn41', 'n_clicks'),
               Input('btn42', 'n_clicks'),
               Input('btn43', 'n_clicks'),
               Input('btn44', 'n_clicks'),
               Input('btn45', 'n_clicks'),
               Input('btn46', 'n_clicks'),
               Input('btn47', 'n_clicks'),
               
               ])

# Function to display the images as modal pop-ups with captions for Plots page
# Todo: possibly make an array/dict with all descriptions with button string as key/index.
def displayImage(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, 
                 btn11, btn12, btn13, btn14, btn15, btn16, btn17, btn18, btn19,
                btn20, btn21, btn22, btn23, btn24, btn25, btn26, btn27, btn28, 
                btn29, btn30, btn31, btn32, btn33, btn34, btn35, btn36, btn37,
               btn38, btn39, btn40, btn41, btn42, btn43, btn44, btn45, btn46, btn47):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #print(changed_id)
    if 'btn1.n_clicks' == changed_id:
        return modal('/assets/plots/best_features.png',
                     'Shows the data distribution of some top features and how they are left skewed.')
    if 'btn2.n_clicks' == changed_id:
        return modal('/assets/plots/correlation.png',
                     'Shows the correlation matrix of all the variables in the data. It can be noted that some of the click stream data has higher correlation with the output variable and demographics has a lower covariance.')
    if 'btn3.n_clicks' == changed_id:
        return modal('/assets/plots/gender.png',
                     'This is a test text.')
    if 'btn4.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_hypertext_agg_count.png',
                     'This is a test text.')
    if 'btn5.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_load_video_agg_count.png',
                     'This is a test text.')
    if 'btn6.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_next_selected_agg_count.png',
                     'This is a test text.')
    if 'btn7.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_page_close_agg_count.png',
                     'This is a test text.')
    if 'btn8.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_percent_progress.png',
                     'Shows that students who ignored filling out demographics information has made more progress, indicating they are more curious to get to the course.')
    if 'btn9.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_problem_check_agg_count.png',
                     'This is a test text.')
    if 'btn10.n_clicks' == changed_id:
        return modal('/assets/plots/gender_vs_problem_graded_agg_count.png',
                     'This is a test text.')
    if 'btn11.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education.png',
                     'This is a test text.')
    if 'btn12.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_hypertext_agg_count.png',
                     'This is a test text.')
    if 'btn13.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_load_video_agg_count.png',
                     'This is a test text.')
    if 'btn14.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_next_selected_agg_count.png',
                     'This is a test text.')
    if 'btn15.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_page_close_agg_count.png',
                     'This is a test text.')
    if 'btn16.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_percent_progress.png',
                     'This is a test text.')
    if 'btn17.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_problem_check_agg_count.png',
                     'This is a test text.')
    if 'btn18.n_clicks' == changed_id:
        return modal('/assets/plots/level_of_education_vs_problem_graded_agg_count.png',
                     'This is a test text.')
    if 'btn19.n_clicks' == changed_id:
        return modal('/assets/plots/percent_progress.png',
                     'Output Variable Distribution shows 75% students completed less than 15% of the course.')
    if 'btn20.n_clicks' == changed_id:
        return modal('/assets/plots/US.png',
                     'This is a test text.')
    if 'btn21.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_hypertext_agg_count.png',
                     'This is a test text.')
    if 'btn22.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_load_video_agg_count.png',
                     'This is a test text.')
    if 'btn23.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_next_selected_agg_count.png',
                     'This is a test text.')
    if 'btn24.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_page_close_agg_count.png',
                     'This is a test text.')
    if 'btn25.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_percent_progress.png',
                     'This is a test text.')
    if 'btn26.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_problem_check_agg_count.png',
                     'This is a test text.')
    if 'btn27.n_clicks' == changed_id:
        return modal('/assets/plots/US_vs_problem_graded_agg_count.png',
                     'This is a test text.')
    if 'btn28.n_clicks' == changed_id:
        return modal('/assets/plots/yob_after.png',
                     'This is a test text.')
    if 'btn29.n_clicks' == changed_id:
        return modal('/assets/plots/yob_before.png',
                     'This is a test text.')
    if 'btn30.n_clicks' == changed_id:
        return modal('/assets/plots/YOB_boxplot_after.png',
                     'This is a test text.')
    if 'btn31.n_clicks' == changed_id:
        return modal('/assets/plots/YOB_boxplot_before.png',
                     'This is a test text.')
    if 'btn32.n_clicks' == changed_id:
        return modal('assets/plots/plots/outlier/num_of_outlier.png',
                     'Shows the outlier heat map.')
    if 'btn33.n_clicks' == changed_id:
        return modal('/assets/plots/plots/gender/gender_education_not_spec.png',
                     'This is a test text.')
    if 'btn34.n_clicks' == changed_id:
        return modal('/assets/plots/plots/gender/gender_ percent_progress.png',
                     'This is a test text.')
    if 'btn35.n_clicks' == changed_id:
        return modal('/assets/plots/plots/education/education_percent_progress.png',
                     'This is a test text.')
    if 'btn36.n_clicks' == changed_id:
        return modal('/assets/plots/plots/education/education_level.png',
                     'This is a test text.')
    if 'btn37.n_clicks' == changed_id:
        return modal('/assets/plots/plots/education/age_vs_not_specified_gender_and_education.png',
                     'This is a test text.')
    if 'btn38.n_clicks' == changed_id:
        return modal('/assets/plots/plots/education/age_level_of_education.png',
                     'This is a test text.')
    if 'btn39.n_clicks' == changed_id:
        return modal('/assets/plots/plots/behavior/stop_vs_next_on_pause.png',
                     'This is a test text.')
    if 'btn40.n_clicks' == changed_id:
        return modal('/assets/plots/plots/behavior/Speed_change_vs_percent_progress.png',
                     'This is a test text.')
    if 'btn41.n_clicks' == changed_id:
        return modal('/assets/plots/plots/behavior/prev_vs_next_vs_percent progress1.png',
                     'This is a test text.')
    if 'btn42.n_clicks' == changed_id:
        return modal('/assets/plots/plots/behavior/pause_on_load.png',
                     'This is a test text.')
    if 'btn43.n_clicks' == changed_id:
        return modal('/assets/plots/plots/behavior/next_pause_vs_gender_and_education_level.png',
                     'This is a test text.')
    if 'btn44.n_clicks' == changed_id:
        return modal('/assets/plots/plots/behavior/next_n_prev_vs_progress_regression1.png',
                     'This is a test text.')
    if 'btn45.n_clicks' == changed_id:
        return modal('/assets/plots/plots/behavior/next_n_prev_vs_progress_regression.png',
                     'This is a test text.')
    if 'btn46.n_clicks' == changed_id:
        return modal('/assets/plots/plots/age/Age_outlier_vs_percent_progress.png',
                     'This is a test text.')
    if 'btn47.n_clicks' == changed_id:
        return modal('/assets/plots/plots/age/Age_distribution_vs_percent_Progress.png',
                     'This is a test text.')

# Modal for the captioned image plots.
def modal(path, desc):
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
            html.P(desc,
                   style = {'font-size' : '150%',
                            'text-align':'center',
                            'display' : 'block'}
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

# Callback to close the modal for plots page
@app.callback(Output('modal', 'style'),
              [Input('modal-close-button', 'n_clicks')])

# Function to close the modal (setting css to disappear)
def close_modal(n):
    if (n is not None):
        return {'display' : 'none'}
    else:
        return {'display' : 'block',
                'overflow': 'scroll'}

# Callback for page routing/changing
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])

# Function for returning certain page contents.
# if adding a new page add an elif like shown and add the file's layout as it's own 
# python file under pages directory.
def display_page(pathname):
    if pathname == '/':
        return index.page_layout
    elif pathname == '/table-data':
        return table_data.page_layout
    elif pathname == '/progress-over-time':
        return progress_over_time.page_layout
    elif pathname == '/resources':
        return resources.page_layout
    elif pathname == '/plots':
        return plots.page_layout
    elif pathname == '/completion':
        return completion.page_layout
    elif pathname == '/completionspring':
        return completionspring.page_layout

if __name__ == '__main__':
    app.run_server(debug=True)
