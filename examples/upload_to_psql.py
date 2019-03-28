"""
There are numerous ways to upload data to a psql database.
Here are a few exampels using the psycopg2 library
Note: for python3
"""

import psycopg2
import datetime
from io import StringIO

with psycopg2.connect(
    host=host,
    user=user,
    password=password,
    dbname=dbname,
) as conn:
    cur = conn.cursor()

    """
    Inserting into a table
    See: http://initd.org/psycopg/docs/usage.html#query-parameters
    """

    cur.execute("""
        INSERT INTO some_table (an_int, a_date, a_string)
        VALUES (%s, %s, %s);
        """,
        (10, datetime.date(2005, 11, 18), "O'Reilly")
    )

    """
    Using the copy_from command you can copy a file-like object easily
    See: http://initd.org/psycopg/docs/cursor.html
    """
    f = StringIO("42\tfoo\n74\tbar\n")
    cur.copy_from(f, 'test', columns=('num', 'data'))
    cur.execute("select * from test where id > 5;")
    # Returns [(6, 42, 'foo'), (7, 74, 'bar')]
    cur.fetchall()
