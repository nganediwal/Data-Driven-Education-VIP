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
ACTIVE_DAYS_TABLE = """
DROP TABLE IF EXISTS edx.student_active_days;
CREATE TABLE edx.student_active_days (
    course_id VARCHAR(255),
    user_id INT,
    week INT,
    n_days_active INT
);
"""

ACTIVE_DAYS_INSERT = """
INSERT INTO edx.student_active_days (course_id, user_id, week, n_days_active)
VALUES %s;
"""
TEMPLATE = "(%(course_id)s, %(user_id)s, %(week)s, %(n_days_active)s)"

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
    day = {'$dayOfWeek': event_date}
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
        {'$addFields': {'week': week, 'day': day}},
        {'$group': {
                '_id': {
                    'course_id': '$context.course_id',
                    'user_id': '$context.user_id',
                    'week': '$week',
                },
                'days': {'$addToSet': '$day'}
            }
        },
        {'$project': {
                '_id': 0,
                'course_id': '$_id.course_id',
                'user_id': '$_id.user_id',
                'week': '$_id.week',
                'n_days_active': {'$size': '$days'},
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
    cur.execute(ACTIVE_DAYS_TABLE)
    psql_conn.commit()
    cur.execute('SELECT course_id, start_ts FROM edx.courses')
    dicts = [{'course_id': course_id, 'start_ts': start_ts} \
        for course_id, start_ts in cur.fetchall()
    ]
    
    mongo_db["course_timestamps"].drop()
    mongo_db["course_timestamps"].insert_many(dicts)

    pipeline = mongo_pipe()
    results = mongo_db['ISYE6501'].aggregate(pipeline)

    execute_values(cur, ACTIVE_DAYS_INSERT, results, template=TEMPLATE)
    psql_conn.commit()

if __name__ == '__main__':
    main()