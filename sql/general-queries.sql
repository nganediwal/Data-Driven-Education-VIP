--General queries for use when cleaning SQL data for ISyE 6501 Fall 2018.

--selecting the course itself
select * from edx.courses where course_id='course-v1:GTx+ISYE6501x+3T2018';

--selecting number of students
select count(id) from edx.auth_user_censored where course_id='course-v1:GTx+ISYE6501x+3T2018' and is_staff=false and is_active=true;

--selecting students who are verified
select user_id, mode, is_active, date_joined, created, last_login
	from (
		(select id, last_login, course_id, date_joined 
			from edx.auth_user_censored 
			where course_id='course-v1:GTx+ISYE6501x+3T2018' 
			and is_staff=false) 
			as isyestudents 
		left join edx.student_courseenrollment 
		on isyestudents.id=edx.student_courseenrollment.user_id and isyestudents.course_id=edx.student_courseenrollment.course_id) 
		as isyestudentcombo
	where mode='verified';

-- inner join on course_id and user_id to get all verified students grades
select isyestudentcombo.user_id, mode, is_active, date_joined, isyestudentcombo.created, last_login,edx.grades_persistentcoursegrade.percent_grade
	from (
		(select id, last_login, course_id, date_joined 
			from edx.auth_user_censored 
			where course_id='course-v1:GTx+ISYE6501x+3T2018' 
			and is_staff=false) 
			as isyestudents 
		left join edx.student_courseenrollment 
		on isyestudents.id=edx.student_courseenrollment.user_id and isyestudents.course_id=edx.student_courseenrollment.course_id) 
		as isyestudentcombo 
	full outer join  edx.grades_persistentcoursegrade on  edx.grades_persistentcoursegrade.user_id = isyestudentcombo.user_id and edx.grades_persistentcoursegrade.course_id ='course-v1:GTx+ISYE6501x+3T2018' 
	where mode='verified' and  edx.grades_persistentcoursegrade.percent_grade > 0.0;