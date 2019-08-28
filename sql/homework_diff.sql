create view isye6501.homework_w_diffs
as
select 
	cur.course_id, 
	cur.user_id, 
	cur.week, 
	cur.time_diff, 
	cur.grade, 
	cur.grade - prev.grade grade_diff
from isye6501.homework prev
join isye6501.homework cur
	on prev.course_id = cur.course_id
	and prev.user_id = cur.user_id
	and prev.week = cur.week-1