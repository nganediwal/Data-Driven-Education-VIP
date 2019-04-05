import pymongo 
import psycopg2

"""
Creates the student_event_counts table for the psql database.
This table contains an aggregation of the count of events by:
    course_id: course_id from edX
    user_id: ...
    week: The time difference in weeks from when the course began and the event
    event_type: ...
    count: The number of times the tuple occurs in the event data

Note: Currently debugging...
"""

MS_PER_WEEK = 1000*3600*24*7
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
    milliseconds = {'$subtract': [course_start_ts, event_date]}
    week = {'$toInt': {'$divide': [milliseconds, MS_PER_WEEK]}}
    pipeline = [
        {'$match': {
            'context': {'course_id': course_id},
            }
        },
        #{'$project': {'week': week}},
        {'$group': {
            '_id': {
                'course_id': '$context.course_id',
                'user_id': '$context.user_id', 
                #'week': '$week',
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

    # Aggregates for each course and uploads to the psql database
    for course_id, course_start_ts in cur.fetchall():
        pipeline = mongo_pipe(course_id, course_start_ts)
        results = list(mongo_db.subset.aggregate(pipeline))
        print(course_id, results)
        for result in results:
            # Unpacks the _id field
            result = {**result['_id'], 'count': result['count']}
            print(result)
            print('test')
            #cur.copy_from(result, 'edx.student_event_counts')
        #psql_conn.commit()

if __name__ == '__main__':
    main()

db.subset.aggregate([
    {'$match': {'context.course_id': "course-v1:GTx+ICT100x+1T2016"}},
    {'$group': { '_id': {'course_id': '$context.course_id', 'user_id': '$context.user_id', 'event_type': '$event_type'}, 'count': {$sum:1}}}])
