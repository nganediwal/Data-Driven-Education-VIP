select *
from (
	select edx.courses.course_id, student_id, student_item_id, submission_id, points_earned, points_possible, created_at, start_ts, TRUNC(DATE_PART('Day', created_at::timestamp -start_ts::timestamp)/7
	from (
		select edx.submissions_studentitem.course_id, student_id, student_item_id, submission_id, points_earned, points_possible, created_at
		from edx.submissions_studentitem join edx.submissions_score
		on edx.submissions_score.submission_id = CAST(edx.submissions_studentitem.id AS INTEGER)
	) st_it
	join edx.courses on st_it.course_id = edx.courses.course_id
) t
where t.course_id like '%%{0}%%'
;