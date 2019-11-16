import connect
import pandas as pd

pipeline = [{ '$group': { '_id': {'author_id':'$author_id', 'week': {'$week':'$created_at'}, 'course_id':'$course_id', 'type':'$_type'},  'ts': {'$first': '$created_at'}, 'total': {'$sum': 1}}},
            { '$sort': {'total': -1 } }]

def get_comments(db):
    posts = [(element['_id']['author_id'], element['_id']['course_id'], element['_id']['week'],  element['ts'], element['_id']['type'], element['total']) for element in db.forum.aggregate(pipeline)]
    df = pd.DataFrame(posts)
    df.columns = ['author_id', 'course_id', 'week', 'ts', 'type' ,'total']
    return df


def aggregate_posts(post_counts):
    pivoted = post_counts.join(post_counts.pivot(index=None, columns='type', values='total'))
    pivoted_pared_down = pivoted[['author_id', 'course_id', 'week', 'ts','Comment', 'CommentThread']]
    aggregate_join = pivoted.loc[pivoted['CommentThread'] >= 0].merge(pivoted.loc[pivoted['Comment'] >= 0], on=['author_id', 'course_id', 'week'], how='outer')
    pared_down = aggregate_join[['author_id','course_id','week','ts_x','Comment_y','CommentThread_x']]
    pared_down.columns = ['user_id', 'course_id', 'week', 'ts','Comment', 'CommentThread']
    pared_down = pared_down.fillna({'Comment':0, 'CommentThread':0})
    return pared_down.loc[pared_down['ts'].notna()]
    
def main():
    db = connect.get_db('forum')
    post_counts = get_comments(db)
    aggregated_posts = aggregate_posts(post_counts)
    print(aggregated_posts)


if __name__ == '__main__':
    main()
