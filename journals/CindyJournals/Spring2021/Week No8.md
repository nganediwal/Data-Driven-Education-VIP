# Week No 8
## 03-10-2021
- Eigth Team Meeting
  - Presentation by students on interactive learning environments
  - Cindy's summary on the Section of "Relevance and cognitive level classification on the Facebook post"
    
    - This section goes over the techniques and approaches they used to classify the relevance and cognitive level of the facebook posts. 
    
    - As a reminder of what as stated earlier, one of the research questions they are trying to answer is "How well does each ML algorithm perform in classifying the Facebook statistics posts in comparison to the relevance and cognitive level coding by human?"
    
    - In order to answer the relevance part of the question, i.e is a post relevant to the course or not, they ran three different ML models, SVM (Support Vector Machine), RF (Random Forest) & ANN (Artificial Neural Network), where for each ML model, a post would either have a score of 0 if not relevant and 1 if relevant. They then decided to sum the scores accross the different models to get a more comparable/objective output. 
    
    - For example, if I posted in the facebook forum asking "Hey are we to use a frequestist or bayesian approach on this data set?" and the SVM  model gave me a score of 1 for relevance, while RF gave me a zero and ANN gave me a 1 then the total relevance score for my post will be 2, which will mean compared to a cours ethat had a zero or one total score I am definitely relevant, but not as relevant as a post that score 3, where every model confirmed it was relevant. 
    
    - In addition to using the scores from these 3 ML models, they also leveraged the assistance of graduated assistants to apply advanced statistical approaches to rank the relevance of the post based on the correlation between the content of the post and the content of the course. This was coded between 0 and 1 for the dichotomous coding and from 0 to 3 for the ordinal coding.
    
    - For the cognitive level part of the question, it gets a little more complicated, where they leverage Bloom’s taxonomy to classify the cognitive level of the past on a scale of 0 to 4 where the range 0-1 is more on the relevance basis, and 2 to 3 involve leveraging knowledge and understand it to apply it to new situations or problems respectively. While the code for 4 will be for creating new concepts. 
    
    - Finally they made use of (KR20) and Cronbach’s alpha to measure the coding consistency between what the ML models classified, and what the grad assistants classified! 
    

## 03-10-2021
- Sixth Sub-team meeting
  - Updates on task progress and overall project structure and next steps
  - Discussed progress done on outlier analysis and reported next steps to the team

## Assignments/ To-Do:
  - Journals (Due every week)
  - Complete outlier handling and missing values ommission
