import connect
import pandas as pd

"""
This is an example script that demonstrates how to connect to the C21U mongo
server and run a simple analysis. See README.md for instructions.

This is an additional example that shows how to swap in your own custom query.
"""

element = "edx.forum.thread.viewed"

pipeline =  [
                { "$match": 
                    {"event_type": element}
                },
                { "$group": { "_id": "$context.user_id", element: {"$sum": 1}}},
                { "$sort": {"total": -1 } }
            ]

# Insert your query here.
def get_cursor(db):
    query = db.ISYE6501.aggregate(pipeline)
    return query

def get_dataframe(db, cursor):
    """Returns a datframe of the results of the query."""
    return pd.DataFrame(list(cursor))

def main():
    db = connect.get_db('clickstream')
    cursor = get_cursor(db)
    dataframe = get_dataframe(db, cursor)
    print(dataframe)
    print(dataframe['name'])

if __name__ == '__main__':
    main()
