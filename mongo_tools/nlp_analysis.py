import connect
from textblob import TextBlob

"""
This is an example script that demonstrates how to connect to the C21U mongo
server and run a simple analysis. See README.md for instructions.
"""


def print_negative_sentiment(db, limit=-0.8):
    """Prints any sentences below the sentiment limit from edX forums."""
    for post in db.forum.find():
        blob = TextBlob(post['body'])
        for sentence in blob.sentences:
            if sentence.sentiment.polarity < limit:
                print(sentence)


def main():
    db = connect.get_db()
    print_negative_sentiment(db)

if __name__ == '__main__':
    main()
