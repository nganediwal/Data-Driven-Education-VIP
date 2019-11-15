import pandas as pd       
import pandas.io.sql as psql
import sqlalchemy as sql

# pip install sqlalchemy
# Need to pipinstall pandas

# create connect string using format, 
# dbtype://username:password@host:port/database  
# fill in the string below
connect_string = 'postgresql://username:password@host:port/database'
# create the engine using the connect string
sql_engine = sql.create_engine(connect_string)

# triple quotes to do multiline query
# Insert query here
query = """

SELECT
	base.course_id,
	base.user_id,
	base.week,
	COALESCE(load_video.count, 0) load_video, -- Note: COALESCE replaces NULLs with 0
	COALESCE(play_video.count, 0) play_video,  -- count is renamed to the relevant column name
	COALESCE(seq_next.count, 0) seq_next,
	COALESCE(problem_check.count, 0) problem_check,
	COALESCE(seq_prev.count, 0) seq_prev,
	COALESCE(seq_goto.count, 0) seq_goto,
	COALESCE(pause_video.count, 0) pause_video,
	Coalesce(problem_save.count, 0) problem_save,
	Coalesce(seek_video.count, 0) seek_video,
	Coalesce(link_clicked.count, 0) link_clicked,
	coalesce(closed_captions_show.count, 0) closed_captions_show,
	coalesce(active_days.n_days_active, 0) active_days,
	coalesce(show_transcript.count, 0) show_transcript,
	coalesce(resume_course.count, 0) resume_course,
	COALESCE(persistent_grade.percent_grade, 0) final_grade
-- Create a stable base to join onto
FROM (
	SELECT DISTINCT
		course_id,
		user_id,
		week
	FROM edx.student_event_counts
	WHERE course_id like '%%ISYE6501%%'
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
LEFT JOIN edx.student_event_counts seq_next
	ON base.course_id = seq_next.course_id
	AND base.user_id = seq_next.user_id
	AND base.week = seq_next.week
	AND seq_next.event_type = 'seq_next'
LEFT JOIN edx.student_event_counts problem_check
	ON  base.course_id = problem_check.course_id 
	AND base.user_id = problem_check.user_id
	AND base.week = problem_check.week
	AND problem_check.event_type = 'problem_check'
LEFT JOIN edx.student_event_counts seq_prev
	ON  base.course_id = seq_prev.course_id
	AND base.user_id = seq_prev.user_id
	AND base.week = seq_prev.week
	AND seq_prev.event_type = 'seq_prev'
LEFT JOIN edx.student_event_counts seq_goto
    ON  base.course_id = seq_goto.course_id
    AND base.user_id = seq_goto.user_id
    AND base.week = seq_goto.week
    AND seq_goto.event_type = 'seq_goto'
LEFT JOIN edx.student_event_counts pause_video
    ON  base.course_id = pause_video.course_id
    AND base.user_id = pause_video.user_id
    AND base.week = pause_video.week
    AND pause_video.event_type = 'pause_video'
LEFT JOIN edx.student_event_counts problem_save
    ON  base.course_id = problem_save.course_id
    AND base.user_id = problem_save.user_id
    AND base.week = problem_save.week
    AND problem_save.event_type = 'problem_save'
LEFT JOIN edx.student_event_counts seek_video
    ON  base.course_id = seek_video.course_id
    AND base.user_id = seek_video.user_id
    AND base.week = seek_video.week
    AND seek_video.event_type = 'seek_video'
LEFT JOIN edx.student_event_counts link_clicked
    ON  base.course_id = link_clicked.course_id
    AND base.user_id = link_clicked.user_id
    AND base.week = link_clicked.week
    AND link_clicked.event_type = 'edx.ui.lms.link_clicked'
LEFT JOIN edx.student_event_counts closed_captions_show
    ON  base.course_id = closed_captions_show.course_id
    AND base.user_id = closed_captions_show.user_id
    AND base.week = closed_captions_show.week
    AND closed_captions_show.event_type = 'edx.video.closed_captions.show'
LEFT JOIN edx.student_event_counts show_transcript
    ON  base.course_id = show_transcript.course_id
    AND base.user_id = show_transcript.user_id
    AND base.week = show_transcript.week
    AND show_transcript.event_type = 'show_transcript'
LEFT JOIN edx.student_event_counts resume_course
    ON  base.course_id = resume_course.course_id
    AND base.user_id = resume_course.user_id
    AND base.week = resume_course.week
    AND resume_course.event_type = 'edx.course.home.resume_course.clicked'
LEFT JOIN edx.grades_persistentcoursegrade persistent_grade
	ON base.course_id = persistent_grade.course_id
	AND base.user_id = persistent_grade.user_id
LEFT JOIN edx.student_active_days active_days
	ON base.course_id = active_days.course_id
	AND base.user_id = active_days.user_id
	AND base.week = active_days.week
--forum views, active days, quiz views, exam views, human-graded quiz pageview
LIMIT 100;
"""

# first param is query, 2nd param is the engine
df = pd.read_sql_query(query, sql_engine)
print(df)
