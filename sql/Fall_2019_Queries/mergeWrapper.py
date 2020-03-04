import connect
import pandas as pd       
import pandas.io.sql as psql
import sqlalchemy as sql
from forum import aggregate_posts, get_comments
import sys
import numpy as np

# pip install sqlalchemy
# Need to pipinstall pandas

def collect_data(course_name, connect_string):

	NANOSECONDS_PER_WEEK = 1000*1000*1000*60*60*24*7

	# create the engine using the connect string
	sql_engine = sql.create_engine(connect_string)

	# triple quotes to do multiline query
	# Insert query here
	query1 = """ 
	SELECT
		base.course_id,
		base.user_id,
		base.week,
		COALESCE(anonID.anonymous_user_id, 00000000000000000000000000000000::varchar) student_id,
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
		WHERE course_id like '%%{0}%%'
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
	LEFT JOIN edx.student_anonymoususerid anonID
		ON base.course_id = anonID.course_id
		AND base.user_id = anonID.user_id
	--forum views, active days, quiz views, exam views, human-graded quiz pageview
	;""".format(course_name)

	query2 = """
	select *
	from (
		select edx.courses.course_id, student_id, student_item_id, submission_id, points_earned, points_possible, created_at, start_ts, TRUNC(DATE_PART('Day', created_at::timestamp -start_ts::timestamp)/7) week
		from (
			select edx.submissions_studentitem.course_id, student_id, student_item_id, submission_id, points_earned, points_possible, created_at
			from edx.submissions_studentitem join edx.submissions_score
			on edx.submissions_score.submission_id = CAST(edx.submissions_studentitem.id AS INTEGER)
		) st_it
		join edx.courses on st_it.course_id = edx.courses.course_id
	) t
	where t.course_id like '%%{0}%%'
	;""".format(course_name)
	# Order by student_id ASC;

	query3 = """
	select course_id, start_ts
	from edx.courses
	;
	"""

	query4 = """
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
		and st.learner_type = 'Verified'
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
	""".format(course_name)

	# first param is query, 2nd param is the engine

	old_weight = 0.5

	# Read SQL queries
	df1 = pd.read_sql_query(query1, sql_engine)
	# df2 = pd.read_sql_query(query2, sql_engine)
	df3 = pd.read_sql_query(query3, sql_engine)
	#df4 = pd.read_sql_query(query4, sql_engine)
	#print("DF4")
	#print(df4)

	#print("\nSQL DATA COLLECTED\n")

	# Get Forum Data From MongoDb, and correct the week calculation
	db = connect.get_db('forum')
	post_counts = get_comments(db)
	forum_output = aggregate_posts(post_counts)
	
	forums_with_start_ts = pd.merge(forum_output, df3, left_on=['course_id'], right_on=['course_id'])
	forums_with_start_ts['week'] = forums_with_start_ts['ts'] - forums_with_start_ts['start_ts']
	forums_with_start_ts = forums_with_start_ts.astype({'week': 'int64'})
	forums_with_start_ts['week'] = forums_with_start_ts['week'] // NANOSECONDS_PER_WEEK
	forums = forums_with_start_ts
	forums = forums.astype({'user_id': 'int32'}).drop(columns=['ts', 'start_ts'])
	print("FORUMS")
	print(forums)

	print("\nMONGODB DATA COLLECTED\n")

	# Perform Merge
	#sql_merge = pd.merge(df1, df4, left_on=['user_id', 'course_id', 'week'], right_on=['user_id', 'course_id','week'])
	#sql_mongo_merge = pd.merge(sql_merge, forums, left_on=['user_id', 'week', 'course_id'], right_on=['user_id', 'week', 'course_id'], how='left').drop(columns=['student_id'])
	
	#df1 = df1.set_index(['user_id', 'course_id', 'week'])
	#df4 = df4.set_index(['user_id', 'course_id', 'week'])
	#df1n4 = df1.join(df4)
	#print("DF1N4")
	#print(df1n4)

	sql_mongo_merge = df1.set_index(['user_id', 'week', 'course_id']).join(forums.set_index(['user_id', 'week', 'course_id']))

	print("DATA MERGED")
	print(sql_mongo_merge)
	print(sql_mongo_merge.columns)

	# Impute
	sql_mongo_merge = sql_mongo_merge.fillna({'time_diff':0, 'Comment':0, 'CommentThread':0})

	# Sort
	sql_mongo_merge = sql_mongo_merge.sort_values(by=['course_id','user_id','week'])

	# Accumulate
	ignore_columns = ['user_id', 'week', 'final_grade', 'course_id']
	avg_columns = list(set(sql_mongo_merge.columns) - set(ignore_columns))
	avg_rows = {}
	for col in avg_columns:
		avg_rows[col] = []

	sql_mongo_merge.set_index(['student_id'])

	for index, row in sql_mongo_merge.iterrows():
		print("\nI\n")
		print(index)
		print("\nR\n")
		print(row)
		for col in avg_columns:
			avg_rows[col].append(sql_mongo_merge.loc[(sql_mongo_merge['week'] <= row['week']) & (sql_mongo_merge['user_id'] == row['user_id']) & (sql_mongo_merge['course_id'] == row['course_id']), col].mean())

	# Add average columns
	for col in avg_columns:
		sql_mongo_merge[col + '_avg'] = avg_rows[col]

	# Remove PII columns
	sql_mongo_merge = sql_mongo_merge.drop(columns=['user_id'])

	print("\nAGGREGATED DATA\n")

	print("SQL MERGE")
	print(sql_mongo_merge)
	print(sql_mongo_merge.columns)

	return sql_mongo_merge

def labeler(x):
    """
    Labels grades with grade numbers.
    """
    if x >= .9:
        return 'A'
    elif (x < .9) and (x >= .8):
        return 'B'
    elif (x < .8) and (x >= .7):
        return 'C'
    elif (x < .7) and (x >= .6):
        return 'D'
    return 'F'

def main():
	course_name = sys.argv[1]
	connect_string = sys.argv[2]
	path = sys.argv[3]
	df = collect_data(course_name, connect_string)
<<<<<<< HEAD
	print("DF")
	print(df)
	dfGroups = df
	dfGroups['letter'] = dfGroups.final_grade.apply(labeler)
	dfGroups = dfGroups.groupby('letter').mean()
	print("Hello")
	print(dfGroups)

	#df.to_csv(path)
=======

	dfA = df.loc[(df['final_grade'] >= 90)]
	dfB = df.loc[(df['final_grade'] >= 80) & (df['final_grade'] < 90)]
	dfC = df.loc[(df['final_grade'] >= 70) & (df['final_grade'] < 80)]

	ListA = np.array([dfA.loc[(df['week'] == 1)], dfA.loc[(df['week'] == 2)], dfA.loc[(df['week'] == 3)], dfA.loc[(df['week'] == 4)], 
		dfA.loc[(df['week'] == 5)], dfA.loc[(df['week'] == 6)], dfA.loc[(df['week'] == 7)], dfA.loc[(df['week'] == 8)],
		dfA.loc[(df['week'] == 9)], dfA.loc[(df['week'] == 10)], dfA.loc[(df['week'] == 11)], dfA.loc[(df['week'] == 12)], 
		dfA.loc[(df['week'] == 13)], dfA.loc[(df['week'] == 14)], dfA.loc[(df['week'] == 15)], dfA.loc[(df['week'] == 16)]])

	ListB = np.array([dfB.loc[(df['week'] == 1)], dfB.loc[(df['week'] == 2)], dfB.loc[(df['week'] == 3)], dfB.loc[(df['week'] == 4)], 
		dfB.loc[(df['week'] == 5)], dfB.loc[(df['week'] == 6)], dfB.loc[(df['week'] == 7)], dfB.loc[(df['week'] == 8)],
		dfB.loc[(df['week'] == 9)], dfB.loc[(df['week'] == 10)], dfB.loc[(df['week'] == 11)], dfB.loc[(df['week'] == 12)], 
		dfB.loc[(df['week'] == 13)], dfB.loc[(df['week'] == 14)], dfB.loc[(df['week'] == 15)], dfB.loc[(df['week'] == 16)]])
	
	ListC = np.array([dfC.loc[(df['week'] == 1)], dfC.loc[(df['week'] == 2)], dfC.loc[(df['week'] == 3)], dfC.loc[(df['week'] == 4)], 
		dfC.loc[(df['week'] == 5)], dfC.loc[(df['week'] == 6)], dfC.loc[(df['week'] == 7)], dfC.loc[(df['week'] == 8)],
		dfC.loc[(df['week'] == 9)], dfC.loc[(df['week'] == 10)], dfC.loc[(df['week'] == 11)], dfC.loc[(df['week'] == 12)], 
		dfC.loc[(df['week'] == 13)], dfC.loc[(df['week'] == 14)], dfC.loc[(df['week'] == 15)], dfC.loc[(df['week'] == 16)]])
		


	df.to_csv(path)
>>>>>>> 28f4eee9220c0b97d9563a79f02819b073800f64


if __name__== "__main__":
	main()