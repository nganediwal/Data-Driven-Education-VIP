select 
	c.course_id, 
	id.user_id,
	((extract(day from ((c.metadata ->> 'submission_due')::timestamp - ct.start_ts)))/7.0)::int week,
	(c.metadata ->> 'submission_due')::timestamp - sub.submitted_at time_diff,
	coalesce(100*(score.points_earned/score.points_possible::float), 0) grade
from edx.course_structure c
join edx.courses ct
	on ct.course_id = c.course_id
	and c.course_id like '%%{0}%%'
	and c.metadata ->> 'display_name' like 'Homework%%'
	and (((c.metadata ->> 'group_access')::jsonb ->> '50')::jsonb ->> 0)::int4 != 1
join edx.student_anonymoususerid id
	on c.course_id = id.course_id
join edx.student_type st
	on st.course_id = c.course_id
	and st.user_id = id.user_id
	and st.learner_type = 'verified'
left join edx.submissions_studentitem si
	on si.course_id = c.course_id
	and c.id = si.item_id
	and id.anonymous_user_id = si.student_id
left join edx.submissions_score score
	on score.course_id = si.course_id
	and score.student_item_id = si.id
	and score.points_possible > 0
left join edx.submissions_submission sub
	on sub.course_id = si.course_id
	and sub.student_item_id = si.id
;