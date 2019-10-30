SELECT
	edx_week.course_id, edx_user.user_id, edx_week.start_ts, edx_week.end_ts, edx_week.week_number, edx_week.week_daterange
INTO jiti.course_user_week
FROM
(WITH week_range as (
	SELECT
		course_id,
		start_ts,
		end_ts,
		generate_series(
			start_ts,
			end_ts,
			'1 week'::interval
		) as week_start_day
	FROM edx.courses
)

SELECT
	course_id,
	start_ts,
	end_ts,
	(date(week_start_day)-date(start_ts))/7 week_number,
	daterange(
		date(week_start_day),
		date(week_start_day + '1 week'::interval),
		'[)') week_daterange
FROM week_range
) edx_week
LEFT JOIN edx.student_type edx_user
	ON edx_user.course_id = edx_week.course_id
WHERE 
	(edx_user.learner_type = 'Verified' OR edx_user.learner_type = 'GT')
	AND edx_user.course_id like '%ISYE6501%'