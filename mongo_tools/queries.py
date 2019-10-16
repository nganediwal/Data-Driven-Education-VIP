import connect
import pandas as pd

"""
This is an example script that demonstrates how to connect to the C21U mongo
server and run a simple analysis. See README.md for instructions.

This is an additional example that shows how to swap in your own custom query.
"""

#element = "page_close"
element = "edx_ui_lms_link_clicked"
pipeline =  [
                { "$match": 
                    {"event_type": "edx.ui.lms.link_clicked"}
                },
                { "$group": { "_id": "$context.user_id", element: {"$sum": 1}}},
                { "$sort": {"total": -1 } }
            ]

# getting all event types
def get_cursor_event_types(db):
    query = db.ISYE6501.find().distinct('event_type') #getting all event types
    return query

#getting pipelined data
def get_cursor(db):
    query = db.ISYE6501.aggregate(pipeline)
    return query

def get_dataframe(db, cursor):
    """Returns a dataframe of the results of the query."""
    print(list(cursor))
    return pd.DataFrame(list(cursor))

def main():
    db = connect.get_db('clickstream')
    cursor = get_cursor(db)
 #   cursor = get_cursor_event_types(db)
    dataframe = get_dataframe(db, cursor)
    print(dataframe)
if __name__ == '__main__':
    main()
