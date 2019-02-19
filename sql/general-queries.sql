--General queries for use when cleaning SQL data for ISyE 6501 Fall 2018.

--selecting the course itself
select * 
from edx.courses 
where course_id='course-v1:GTx+ISYE6501x+3T2018';

--selecting number of students
select e.mode, c.name cohort, count(*) 
from edx.student_courseenrollment e
join edx.course_groups_cohortmembership c
	on c.user_id = e.user_id
	and c.course_id = e.course_id
	and e.course_id = 'course-v1:GTx+ISYE6501x+3T2018'
group by e.mode, c.name;

--selecting students who are verified
select e.user_id, e.mode, e.is_active, u.date_joined, e.created, u.last_login
from edx.student_courseenrollment e
join edx.auth_user_censored u
	on u.id = e.user_id
	and u.course_id = e.course_id
	and u.course_id = 'course-v1:GTx+ISYE6501x+3T2018'
	and e.mode = 'verified'
	and u.is_staff = false

-- inner join on course_id and user_id to get all verified students grades
select g.user_id, e.mode, e.is_active, u.is_active, u.last_login, g.percent_grade
from edx.grades_persistentcoursegrade g
join edx.student_courseenrollment e
	on g.user_id = e.user_id
	and g.course_id = e.course_id
	and g.course_id = 'course-v1:GTx+ISYE6501x+3T2018'
	and e.mode = 'verified'
	and g.percent_grade > 0.0
join edx.auth_user u
	on g.user_id = u.id
	and g.course_id = u.course_id
	and g.course_id = 'course-v1:GTx+ISYE6501x+3T2018'