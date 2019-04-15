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

Note: We only consider events from the browser 
(actual clicks, not processing done on the server)
"""

MS_PER_WEEK = 1000*60*60*24*7
EVENT_COUNT_TABLE = """
DROP TABLE IF EXISTS edx.student_event_counts;
CREATE TABLE edx.student_event_counts (
    course_id VARCHAR(255),
    user_id INT,
    week INT,
    event_type VARCHAR(255),
    count INT
);
"""

EVENT_COUNTS_INSERT = """
INSERT INTO edx.student_event_counts (course_id, user_id, week, event_type, count)
VALUES %s;
"""
TEMPLATE = "(%(course_id)s, %(user_id)s, %(week)s, %(event_type)s, %(count)s)"

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

def mongo_pipe():
    # Setting up our week calculation
    event_date = {"$dateFromString": {"dateString": "$time"}}
    milliseconds = {'$subtract': [event_date, '$timestamps.start_ts']}
    week = {'$toInt': {'$divide': [milliseconds, MS_PER_WEEK]}}
    pipeline = [
        # Include only browser events (i.e., events from the user)
        {'$match': {
            'event_source': 'browser',
            'context.user_id': {'$ne': None}
            }
        },
        # Join the course_timestamps data
        {'$lookup': {
                'from': 'course_timestamps',
                'localField': 'context.course_id',
                'foreignField': 'course_id',
                'as': 'timestamps'
            }
        },
        # Lookup returns a single valued list so we unwind it
        {'$unwind': '$timestamps'},
        {'$addFields': {'week': week}},
        {'$match': {'week': {'$gte': 0}}},
        {'$group': {
                '_id': {
                    'course_id': '$context.course_id',
                    'user_id': '$context.user_id',
                    'week': '$week',
                    'event_type': '$event_type'
                },
                'count': {'$sum': 1}
            }
        }
    ]
    return pipeline

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
    dicts = [{'course_id': course_id, 'start_ts': start_ts} \
        for course_id, start_ts in cur.fetchall()
    ]
    
    mongo_db["course_timestamps"].drop()
    mongo_db["course_timestamps"].insert_many(dicts)

    pipeline = mongo_pipe()
    results = mongo_db['ISYE6501'].aggregate(pipeline)

    # Lazily unpacks the results
    results = map(lambda r: {**r['_id'], 'count': r['count']}, results)
    execute_values(cur, EVENT_COUNTS_INSERT, results, template=TEMPLATE)
    psql_conn.commit()

if __name__ == '__main__':
    main()