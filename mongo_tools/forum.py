import connect
import pandas as pd

pipeline = [{ '$group': { '_id': {'author_id':'$author_id', 'week': {'$week': '$created_at'}, 'course_id':'$course_id'}, 'total': {'$sum': 1}}},
            { '$sort': {'total': -1 } }]

def print_posts(db):
    """Prints any sentences below the sentiment limit from edX forums."""
    # return [(element['_id']['author_id'], element['_id']['course_id'], element['_id'][2], element['total']) for element in db.forum.aggregate(pipeline)]
    return [(element['_id']['author_id'], element['_id']['course_id'], element['_id']['week'], element['total']) for element in db.forum.aggregate(pipeline)]
    # return db.forum.find();

def main():
    db = connect.get_db('forum')
    posts = print_posts(db)
    df = pd.DataFrame(posts)
    df.columns = ['author_id', 'course_id', 'week', 'total']
    print(df)
    # print(db.forum.aggregate([{ '$group': { '_id': 'type', 'total': {'$sum': 1}}},
            # { '$sort': {'total': -1 } }]))

if __name__ == '__main__':
    main()
