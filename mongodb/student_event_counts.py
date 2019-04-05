import pymongo 
import psycopg2
from psycopg2.extras import execute_values

"""
Creates the student_event_counts table for the psql database.
This table contains an aggregation of the count of events by:
    course_id: course_id from edX
    user_id: ...
    week: The time difference in weeks from when the course began and the event
    event_type: ...
    count: The number of times the tuple occurs in the event data

Note: We only consider events from the browser (actual clicks,
not processing done on the server)
"""

MS_PER_WEEK = 1000*60*60*24*7
EVENT_COUNT_TABLE = """
DROP TABLE IF EXISTS edx.student_event_counts;
CREATE TABLE edx.student_event_counts (
    course_id VARCHAR(255),
    week INT,
    user_id INT,
    event_type VARCHAR(255),
    count INT
);
"""

EVENT_COUNTS_INSERT = """
INSERT INTO edx.student_event_counts (course_id, week, user_id, event_type, count)
VALUES %s;
"""
SNIPPET = "(%(course_id)s, %(week)s, %(user_id)s, %(event_type)s, %(count)s)"

def get_creds(credentials_filename):
    creds = open(credentials_filename, 'r').read()
    host, username, password, dbname = creds.split()
    return {
        'host': host,
        'username': username,
        'password': password,
        'dbname': dbname
    }

def get_mongo_db(creds):
    client = pymongo.MongoClient(creds['host'], 27017)
    db = client[creds['dbname']]
    db.authenticate(creds['username'], creds['password'])
    return db

def get_psql_conn(creds):
    conn = psycopg2.connect(
        host=creds['host'],
        user=creds['username'],
        password=creds['password'],
        dbname=creds['dbname']
    )
    return conn

def mongo_pipe(course_id, course_start_ts):
    event_date = {"$dateFromString": {"dateString": "$time"}}
    milliseconds = {'$subtract': [event_date, course_start_ts]}
    week = {'$toInt': {'$divide': [milliseconds, MS_PER_WEEK]}}
    pipeline = [
        {
            '$match': {
                'context.course_id': course_id,
                'context.user_id': {
                    '$exists': 'true'
                },
                'event_source': 'browser',
            }
        },
        {
            '$addFields': {
                'week': week
            }
        },
        {
            '$match': {'week': {'$gt': 0}}
        },
        {
            '$group': {
                '_id': {
                    'course_id': '$context.course_id',
                    'week': '$week',
                    'user_id': '$context.user_id',
                    'event_type': '$event_type'
                },
                'count': {'$sum': 1}
            }
        }
    ]
    return pipeline

def insert_data(conn, insert, data):
    curs = conn.cursor()
    for datum in data:
        curs.execute(insert, datum)
    conn.commit()

def main():
    # Setting up by loading credentials and connections
    mongo_creds = get_creds('../creds/mongo_creds.txt')
    psql_creds = get_creds('../creds/psql_creds.txt')
    mongo_db = get_mongo_db(mongo_creds)
    psql_conn = get_psql_conn(psql_creds)

    # Creates the table in the psql database and selects course_id, start_ts
    cur = psql_conn.cursor()
    cur.execute(EVENT_COUNT_TABLE)
    psql_conn.commit()
    cur.execute('SELECT course_id, start_ts FROM edx.courses')

    # Aggregates for each course and uploads to the psql database
    for course_id, course_start_ts in cur.fetchall():
        pipeline = mongo_pipe(course_id, course_start_ts)
        results = mongo_db.subset.aggregate(pipeline)

        # Lazily unpacks the _id field
        results = map(lambda r: {**r['_id'], 'count': r['count']}, results)

        # Uploads to database
        execute_values(cur, EVENT_COUNTS_INSERT, results, template=SNIPPET)
        psql_conn.commit()
        print(f'Done with: {course_id}')

if __name__ == '__main__':
    main()