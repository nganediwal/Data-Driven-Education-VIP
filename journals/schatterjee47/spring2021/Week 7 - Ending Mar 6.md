# Week 7 Ending 3/6

## Team Meeting(3rd Mar):
  - Learned about Analytics Research Highlights for two seperate reseach project
  - OMSA Applicant Success Prediction Project
    - Research Target: 
      - Can we predict whether an applicant will be admitted?
      - Which application features predict successful admission?
    - Methods
      - Logistic Regression
      - Random Forest
      - Gradient Boosting : Best Model with ROC-AUC score of 0.81 and standard deviation of 0.01
      - ADABoostClassification
    - The applicants’ GPA played the most important role for being admitted to the program, followed by the duration that the applicant spent in a college and then Fulfilling a bachelor’s degree and having strong reference letters.
    - Reduced number of features and identified key input variables(154)
    - Future Work
      - Model the successful completion
      - Predict students’ grades in three core courses
      - Build models predicting various success metrics
  - Analyzing MOOC Environment Using Clickstream Data
    - Conventional metrics such as final grade is not accurately capture the experiences of learners hence the need to use alternative measures, such as usage patterns in exploring course content
    - How do learners from various demographic backgrounds (e.g., gender, language)interact with a MOOC environment?
    - How is learners’ interaction with the MOOC courseware related to their course engagement?
    - Data Findings:
      - 20% female & 79% male students, 29% came from USA, 37% holding Bachelor’s degree & 27% Master’s or professional degrees
      - On average, enrolled students completed 13% of total content & stayed active for 6.6 weeks
      - Only 5% of total enrolled students were “explorer"
    - Some interesting findings 
      - Female students seem to be more responsive to course navigation features
      - Patterns of navigating course content may be associated with different learning outcomes depending on language background

## TODO Tasks:
  - Explore feature importance
  - Analyze the data to some up with trends in the data. Represent them in plots.
  - Complete Mid Term Peer Evaluation
  - Update Trello Board based on discussion
  
## Sub-team meeting(3rd Mar):'
  - Discussed on the plan of using the new data model in the UI if time permits. 
  - Explained the data science team about the new project structure of the data model development
	- Cindy to work on null data and outlier clean up. Stub methods exists in the code and needs to be coded with actual findings
	- Lindsey to work on data aggregations and prepare the data for running initial models
  - Discussed options to train two types of model.
  	- Traditional supervised learning model with Week as an input feature
	- Recurrent Neural Network for using week as a time series prediction.
  - UI Team updates:
  	- Ania has documented her research interview with Sonam. She will now setup the UI app and create a proposal on how the UI/wireframes should be modified to achieve immidiate goals
	- Attush has made progress on the css bootstrap and will demo the app in the next sub team meeting.
	- Aashay has reviewed the LTI integration document and will setup a call with Kenith to setup his enviornment. 

## Work Completed
  - Added code to join the demographics, clickstream and output data into 1 pandas dataframe
  - Add more code to do data analysis and produced interesting graphs on Demographics distributions
  - Added code to generate percentile numbers on the output variable
  - Completed Mid Term Peer Evaluation
  - Updated Trello Board based on the sub team meeting discussion and tasks
  - Git Link: https://github.gatech.edu/C21U/vip-research/tree/master/spring2021_model