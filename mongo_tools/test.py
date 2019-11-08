import connect
import pandas as pd

"""
This is an example script that demonstrates how to connect to the C21U mongo
server and run a simple analysis. See README.md for instructions.

This is an additional example that shows how to swap in your own custom query.
"""

# count the events per person, per event_type, per week

# ultimate out put is a table, with user id + week itself
# edx clickstream data

# weeks script needs to take in data for all semesters

# Print out final dataframe in Panda's format, which has key composed of
# Person's ID, relative week, and event counts, and semester
# Columns: Person's ID, relative week, event_type, semester

element = "edx_forum_thread_viewed"

pipeline =  [
                { "$match": 
                    {"event_type": element} ## events that match type element
                }#,
                # { "$group": { "_id": "$context.user_id", element: {"$sum": 1}}},
                #     # groups by user_id
                # { "$sort": {"total": -1 } } # Decreasomg order
            ]

# Insert your query here.
def get_cursor(db):
    query = db.ISYE6501.find(pipeline)
    #query = db.ISYE6501.find()
    return query

def get_dataframe(db, cursor):
    """Returns a datframe of the results of the query."""
    return pd.DataFrame(list(cursor))

def main():
    db = connect.get_db('clickstream')
    cursor = get_cursor(db)
    dataframe = get_dataframe(db, cursor)
    print(dataframe)
    print(dataframe['event_type'])

if __name__ == '__main__':
    main()
