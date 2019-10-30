-- Remove the table in case there are updates
DROP TABLE IF EXISTS jiti.event_dataframe;

SELECT
	base.course_id,
	base.user_id,
	base.week,
	COALESCE(load_video.count, 0) load_video, -- Note: COALESCE replaces NULLs with 0
	COALESCE(play_video.count, 0) play_video  -- count is renamed to the relevant column name
INTO jiti.event_dataframe -- Save to a table (you have write access in the jiti schema)
-- Create a stable base to join onto
FROM (
	SELECT DISTINCT
		course_id,
		user_id,
		week
	FROM edx.student_event_counts
	WHERE course_id like '%ISYE6501%'
) base
-- A left join preserves the index of the base
LEFT JOIN edx.student_event_counts load_video
    -- First, join on the three keys
	ON  base.course_id = load_video.course_id
	AND base.user_id = load_video.user_id
	AND base.week = load_video.week
    -- Then, filter all irrelevant event types
	AND load_video.event_type = 'load_video'
LEFT JOIN edx.student_event_counts play_video
	ON  base.course_id = play_video.course_id -- Make sure to use the correct table alias here!
	AND base.user_id = play_video.user_id
	AND base.week = play_video.week
	AND play_video.event_type = 'play_video'
;