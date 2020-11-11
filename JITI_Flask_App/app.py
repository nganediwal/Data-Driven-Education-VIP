# -*- coding: utf-8 -*-
from pages import index, plots, progress_over_time, resources, table_data
from globalvars import *

print(dcc.__version__) # 0.6.0 or above is required

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
                dbc.NavLink("Plots", href = "plots", id = "Plots"),
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




## TODO: Put all the attributes into a list, iterate through and display student values
## Basically, display their stats and make it look nicer

## TODO: Iterate through student attributes in callback, update the "weakness" message 
# depending on what's below average

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
               Input('btn21', 'n_clicks'),])
def displayImage(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, 
                 btn11, btn12, btn13, btn14, btn15, btn16, btn17, btn18, btn19,
                btn20, btn21, btn22, btn23, btn24, btn25, btn26, btn27, btn28, 
                btn29, btn30, btn31):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #print(changed_id)
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
        return index.page_layout
    elif pathname == '/table-data':
        return table_data.page_layout
    elif pathname == '/progress-over-time':
        return progress_over_time.page_layout
    elif pathname == '/resources':
        return resources.page_layout
    elif pathname == '/plots':
        return plots.page_layout

if __name__ == '__main__':
    app.run_server(debug=True)