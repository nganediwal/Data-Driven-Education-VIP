-- Selects all exams for ISYE650
select 
	g.course_id,
	g.user_id,
	g.earned_graded,
	g.possible_graded,
	c.metadata ->> 'display_name' display_name, 
	(c.metadata ->> 'due')::timestamp - g.first_attempted::timestamp difference,
	((extract(day from (g.first_attempted - ct.start_ts)))/7.0)::int week,
from edx.grades_persistentsubsectiongrade g
join edx.course_structure c
	on c.course_id = g.course_id
	and c.course_id like '%ISYE6501%3T2018%'
	and c.id = g.usage_key
	and g.possible_graded != 0
	and g.first_attempted is not null
	and c.metadata ->> 'due' is not null
join edx.student_type s
	on g.course_id = s.course_id
	and g.user_id = s.user_id
	and s.learner_type = 'Verified'
join edx.courses ct
	on ct.course_id = g.course_id
