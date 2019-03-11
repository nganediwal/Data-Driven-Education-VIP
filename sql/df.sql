-- The dataframe used to train our models. Based on Gardner+Brooks2018
DROP TABLE IF EXISTS edx.dataframe CASCADE;

CREATE TABLE edx.dataframe (
    id VARCHAR(255) PRIMARY KEY,
    course_id VARCHAR(255),
    user_id VARCHAR(255),
    week INT,
    clickstream_forum_views INT,
    clickstream_active_days SMALLINT,
    clickstream_quiz_views INT,
    clickstream_exam_views INT,
    clickstream_quiz_peer_views INT,
    quiz_lead_time INT,
    quiz_raw_points INT,
    quiz_avg_score NUMERIC,
    quiz_raw_points_per_submission NUMERIC,
    quiz_n_submissions INT,
    quiz_percent_allowed_submissions NUMERIC,
    quiz_percent_max_submissions NUMERIC,
    quiz_percent_corrent_submissions NUMERIC,
    quiz_weekly_delta NUMERIC,
    forum_posts INT,
    forum_replies INT,
    forum_avg_sentiment NUMERIC,
    forum_avg_post_length NUMERIC,
    forum_n_positive INT,
    forum_n_negative INT,
    forum_n_neutral INT,
    forum_sentiment_delta NUMERIC,
    forum_n_threads INT,
    forum_n_words_bigrams INT,
    forum_f_reading_ease INT,
    forum_fk_readling_level INT,
    forum_net_votes INT
);

COMMENT ON COLUMN edx.dataframe.week IS 'The week number of the course';
COMMENT ON COLUMN edx.dataframe.clickstream_forum_views IS 'Number of pageviews of forum pages';
COMMENT ON COLUMN edx.dataframe.clickstream_active_days IS 'Number of days for which user registered any clickstream activity (maximum of 7)';
COMMENT ON COLUMN edx.dataframe.clickstream_quiz_views IS 'Number of pageviews of quiz attempt pages, as measured by clickstream features';
COMMENT ON COLUMN edx.dataframe.clickstream_exam_views IS 'Number of pageviews of exam-type quiz pages, as measured by clickstream features';
COMMENT ON COLUMN edx.dataframe.clickstream_quiz_peer_views IS 'Number  of  pageviews  of  human-graded  quiz  pages,  as  measured  by clickstream features';
COMMENT ON COLUMN edx.dataframe.quiz_lead_time IS 'Time between a quiz submission and deadline for all submissions; discretized buckets for t≥7 days (2), 3≤t<7 (1), 1≤t<3, 0≤t<1 (0), and late (-1)';
COMMENT ON COLUMN edx.dataframe.quiz_raw_points IS 'Sum of total raw points earned on quizzes';
COMMENT ON COLUMN edx.dataframe.quiz_avg_score IS 'Average raw score on all assignments';
COMMENT ON COLUMN edx.dataframe.quiz_raw_points_per_submission IS 'Total raw points divided by total submissions';
COMMENT ON COLUMN edx.dataframe.quiz_n_submissions IS 'Total count of quiz submissions';
COMMENT ON COLUMN edx.dataframe.quiz_percent_allowed_submissions IS 'Total count of quiz submissions as a percent of the maximum allowed submissions';
COMMENT ON COLUMN edx.dataframe.quiz_percent_max_submissions IS 'A student total number of quiz submissions as a percent of themaximum number of submissions made by any student in the course';
COMMENT ON COLUMN edx.dataframe.quiz_percent_corrent_submissions IS 'Percentage of the total submissions that were correct';
COMMENT ON COLUMN edx.dataframe.quiz_weekly_delta IS 'Difference between current week average and previous week average quizgrade';
COMMENT ON COLUMN edx.dataframe.forum_posts IS 'Total number of posts';
COMMENT ON COLUMN edx.dataframe.forum_replies IS 'Number of posts by user that were replies to other users (i.e., not to themselves, and notthe first post in the thread)';
COMMENT ON COLUMN edx.dataframe.forum_avg_sentiment IS 'Average net sentiment of posts (positive – negative); Hutto & Gilbert 2014';
COMMENT ON COLUMN edx.dataframe.forum_avg_post_length IS 'Average length of posts, in characters';
COMMENT ON COLUMN edx.dataframe.forum_n_positive IS 'Number of posts with net sentiment≥1 standard deviation above thread average';
COMMENT ON COLUMN edx.dataframe.forum_n_negative IS 'Number of posts with net sentiment≤−1 standard deviation below thread average';
COMMENT ON COLUMN edx.dataframe.forum_n_neutral IS 'Number of posts with net sentiment within 1 standard deviation of thread average';
COMMENT ON COLUMN edx.dataframe.forum_sentiment_delta IS 'Average of (post sentiment – avg sentiment for thread)';
COMMENT ON COLUMN edx.dataframe.forum_n_threads IS 'Total number of threads initiated by student';
COMMENT ON COLUMN edx.dataframe.forum_n_words_bigrams IS 'Count of unique words/bigrams used across all posts';
COMMENT ON COLUMN edx.dataframe.forum_f_reading_ease IS 'Flesch Reading Ease score, discretized into separate features in increments of 10 from 0 to 100 (Kincaid et al., 1975)';
COMMENT ON COLUMN edx.dataframe.forum_fk_readling_level IS 'Flesch-Kincaid grade level, discretized into separate features in increments of1 from 0 to 20 (Kincaid et al., 1975)';
COMMENT ON COLUMN edx.dataframe.forum_net_votes IS 'Total net upvotes users’ posts received (positive – negative)';
GRANT SELECT ON edx.dataframe TO edx_student;