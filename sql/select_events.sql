
--selecting all events
SELECT L.course_id, L.user_id, L.week, seq_next_count, seq_prev_count, seq_goto_count, play_video_count, pause_video_count, closed_captions_show_count, problem_save_count, seek_video_count, link_clicked_count
FROM
((SELECT course_id, user_id, week
FROM ((SELECT course_id, user_id, week FROM edx.student_event_counts WHERE event_type = 'seq_next') UNION
	 (SELECT course_id, user_id, week FROM edx.student_event_counts WHERE event_type = 'seq_prev') UNION
	 (SELECT course_id, user_id, week FROM edx.student_event_counts WHERE event_type = 'seq_goto') UNION
	 (SELECT course_id, user_id, week FROM edx.student_event_counts WHERE event_type = 'play_video') UNION
	 (SELECT course_id, user_id, week FROM edx.student_event_counts WHERE event_type = 'pause_video') UNION
	 (SELECT course_id, user_id, week FROM edx.student_event_counts WHERE event_type = 'edx.video.closed_captions.show') UNION
	 (SELECT course_id, user_id, week FROM edx.student_event_counts WHERE event_type = 'problem_save') UNION
	 (SELECT course_id, user_id, week FROM edx.student_event_counts WHERE event_type = 'seek_video') UNION
	 (SELECT course_id, user_id, week FROM edx.student_event_counts WHERE event_type = 'edx.ui.lms.link_clicked')) AS L) AS L
LEFT JOIN
(SELECT course_id, user_id, week, count AS seq_next_count FROM edx.student_event_counts WHERE event_type = 'seq_next') T1
ON L.course_id = T1.course_id AND L.user_id = T1.user_id AND L.week = T1.week
LEFT JOIN
(SELECT course_id, user_id, week, count AS seq_prev_count FROM edx.student_event_counts WHERE event_type = 'seq_prev') T2
ON L.course_id = T2.course_id AND L.user_id = T2.user_id AND L.week = T2.week
LEFT JOIN
(SELECT course_id, user_id, week, count AS seq_goto_count FROM edx.student_event_counts WHERE event_type = 'seq_goto') T3
ON L.course_id = T3.course_id AND L.user_id = T3.user_id AND L.week = T3.week
LEFT JOIN
(SELECT course_id, user_id, week, count AS play_video_count FROM edx.student_event_counts WHERE event_type = 'play_video') T4
ON L.course_id = T4.course_id AND L.user_id = T4.user_id AND L.week = T4.week
LEFT JOIN
(SELECT course_id, user_id, week, count AS pause_video_count FROM edx.student_event_counts WHERE event_type = 'pause_video') T5
ON L.course_id = T5.course_id AND L.user_id = T5.user_id AND L.week = T5.week
LEFT JOIN
(SELECT course_id, user_id, week, count AS closed_captions_show_count FROM edx.student_event_counts WHERE event_type = 'edx.video.closed_captions.show') T6
ON L.course_id = T6.course_id AND L.user_id = T6.user_id AND L.week = T6.week
LEFT JOIN
(SELECT course_id, user_id, week, count AS problem_save_count FROM edx.student_event_counts WHERE event_type = 'problem_save') T7
ON L.course_id = T7.course_id AND L.user_id = T7.user_id AND L.week = T7.week
LEFT JOIN
(SELECT course_id, user_id, week, count AS seek_video_count FROM edx.student_event_counts WHERE event_type = 'seek_video') T8
ON L.course_id = T8.course_id AND L.user_id = T8.user_id AND L.week = T8.week
LEFT JOIN
(SELECT course_id, user_id, week, count AS link_clicked_count FROM edx.student_event_counts WHERE event_type = 'edx.ui.lms.link_clicked') T9
ON L.course_id = T9.course_id AND L.user_id = T9.user_id AND L.week = T9.week
)


--ACTUAL STATS QUERY
SELECT course_id, event_type, (stats_agg(count)).kurtosis, (stats_agg(count)).variance, SUM(count)
FROM edx.student_event_counts
GROUP BY course_id, event_type
ORDER BY SUM;


--DEFINING THE STATS_AGG FUNCTION (RUN THIS FIRST)
--https://github.com/ellisonch/PostgreSQL-Stats-Aggregate/blob/master/pg_stats_aggregate.sql
create type _stats_agg_accum_type AS (
	n bigint,
	min double precision,
	max double precision,
	m1 double precision,
	m2 double precision,
	m3 double precision,
	m4 double precision
);

create type _stats_agg_result_type AS (
	count bigint,
	min double precision,
	max double precision,
	mean double precision,
	variance double precision,
	skewness double precision,
	kurtosis double precision
);

create or replace function _stats_agg_accumulator(_stats_agg_accum_type, double precision)
returns _stats_agg_accum_type AS '
DECLARE
	a ALIAS FOR $1;
	x alias for $2;
	n1 bigint;
	delta double precision;
	delta_n double precision;
	delta_n2 double precision;
	term1 double precision;
BEGIN
	n1 = a.n;
	a.n = a.n + 1;
	delta = x - a.m1;
	delta_n = delta / a.n;
	delta_n2 = delta_n * delta_n;
	term1 = delta * delta_n * n1;
	a.m1 = a.m1 + delta_n;
	a.m4 = a.m4 + term1 * delta_n2 * (a.n*a.n - 3*a.n + 3) + 6 * delta_n2 * a.m2 - 4 * delta_n * a.m3;
	a.m3 = a.m3 + term1 * delta_n * (a.n - 2) - 3 * delta_n * a.m2;
	a.m2 = a.m2 + term1;
	a.min = least(a.min, x);
	a.max = greatest(a.max, x);
	RETURN a;
END;
'
language plpgsql;

create or replace function _stats_agg_finalizer(_stats_agg_accum_type)
returns _stats_agg_result_type AS '
BEGIN
	RETURN row(
		$1.n, 
		$1.min,
		$1.max,
		$1.m1,
		$1.m2 / ($1.n - 1.0), 
		case when $1.m2 = 0 then null else sqrt($1.n) * $1.m3 / ($1.m2 ^ 1.5) end, 
		case when $1.m2 = 0 then null else $1.n * $1.m4 / ($1.m2 * $1.m2) - 3.0 end
	);
END;
'
language plpgsql;

create aggregate stats_agg(double precision) (
	sfunc = _stats_agg_accumulator,
	stype = _stats_agg_accum_type,
	finalfunc = _stats_agg_finalizer,
	initcond = '(0,,, 0, 0, 0, 0)'
);