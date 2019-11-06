# Meeting Notes 
## Todays TO-DO
* Identify the amount of given assignments a student submits a week 
  * Currently looking into the submissions_studentitem and submissions_score tables to do so
  * The following snipet of a query has helped me only get a look at ISYE course information
  * Select *
    From edx.submissions_studentitem
    Where course_id like '%ISYE6501%'
  * Creating a query with 
      ^ Student id 
      ^ course id
      ^ week of the year 
      ^ Total
      
