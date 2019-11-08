select course_id, user_id, percent_grade, letter_grade, passed_timestamp
from edx.grades_persistentcoursegrade
/* < 0.7 : not pass 
   >= 0.7 : pass */
where percent_grade < 0.7
limit 500
