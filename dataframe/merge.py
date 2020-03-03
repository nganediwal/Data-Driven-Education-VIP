import connect
import pandas as pd
import pandas.io.sql as psql
import sqlalchemy as sql
from forum import aggregate_posts, get_comments
import sys

NANOSECONDS_PER_WEEK = 1000_000_000*60*60*24*7


def sql_dataframes(course_name, connect_string):
    # create the engine using the connect string
    sql_engine = connect.sql_engine()

    # To Do: Name queries based on what they're doing
    query1 = open('sql/query1.sql').read().format(course_name)
    query2 = open('sql/query2.sql').read().format(course_name)
    query3 = open('sql/query3.sql').read()
    query4 = open('sql/query4.sql').read().format(course_name)

    # Read SQL queries
    df1 = pd.read_sql_query(query1, sql_engine)
    df3 = pd.read_sql_query(query3, sql_engine)
    df4 = pd.read_sql_query(query4, sql_engine)

    return df1, df3, df4


def mongo_dataframe():
    # Get Forum Data From MongoDb, and correct the week calculation
    db = connect.get_db('forum')
    post_counts = get_comments(db)
    forum_output = aggregate_posts(post_counts)

    forums_with_start_ts = pd.merge(forum_output, df3,
                                    left_on=['course_id'],
                                    right_on=['course_id'])
    forums_with_start_ts['week'] = \
        forums_with_start_ts['ts'] - forums_with_start_ts['start_ts']
    forums_with_start_ts = forums_with_start_ts.astype({'week': 'int64'})
    # Integer divide (no rounding)
    forums_with_start_ts['week'] = \
        forums_with_start_ts['week'] // NANOSECONDS_PER_WEEK
    forums = forums_with_start_ts
    forums = forums.astype({'user_id': 'int32'}) \
        .drop(columns=['ts', 'start_ts'])
    return forums


def merge_dataframes(df1, df2, df3, forums):
    # Perform Merge
    sql_merge = pd.merge(
        df1, df4,
        left_on=['user_id', 'course_id', 'week'],
        right_on=['user_id', 'course_id', 'week']
    )
    sql_mongo_merge = pd.merge(
        sql_merge, forums,
        left_on=['user_id', 'week', 'course_id'],
        right_on=['user_id', 'week', 'course_id'],
        how='left'
    ).drop(columns=['student_id'])
    return sql_mongo_merge


def process_dataframe(df):
    """
    Imputes data and computes the cumulative average numerical columns.
    """
    # Impute
    df = df.fillna(
        {'time_diff': 0, 'Comment': 0, 'CommentThread': 0}
    )

    # Sort
    df = df.sort_values(by=['course_id','user_id','week'])

    # Define columns to average
    ignore_columns = ['user_id', 'week', 'final_grade', 'course_id']
    avg_columns = list(set(sql_mongo_merge.columns) - set(ignore_columns))

    # Find the cumulative average by finding the cumulative sum of the sorted
    # dataframe and then dividing by the week number plus 1
    # (since week 0 is the first week)
    avg_df = df \
        .groupby(['course_id', 'user_id'])[avg_columns] \
        .cumsum() \
        .div(sql_mongo_merge.week+1, axis=0)
    # append _avg to each column
    avg_df.columns = [col + '_avg' for col in avg_df.columns]
    # add the averaged columns to original dataframe
    df = sql_mongo_merge.join(avg_df)
    return df


def collect_data(course_name, connect_string):
    df1, df3, df4 = sql_dataframes(course_name, connect_string)
    print("\nSQL DATA COLLECTED\n")
    forums = mongo_dataframe()
    print("\nMONGODB DATA COLLECTED\n")
    df = merge_dataframes(df1, df3, df4, forums)
    print("\nDATA MERGED\n")
    df = process_dataframe(df)
    print("\nAGGREGATED DATA\n")
    return df


def main():
    course_name = sys.argv[1]
    connect_string = sys.argv[2]
    path = sys.argv[3]
    df = collect_data(course_name, connect_string)
    df.to_csv(path)


if __name__ == "__main__":
    main()
