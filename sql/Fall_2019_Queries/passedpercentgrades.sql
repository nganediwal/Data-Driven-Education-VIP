-- This query only features those that passed 
Select course_id, user_id, percent_grade, letter_grade, passed_timestamp
From edx.grades_persistentcoursegrade
/* < 0.7 : not pass 
	>= 0.7 : pass */
where percent_grade >= .7
