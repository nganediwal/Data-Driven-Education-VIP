"""
Example credentials file, fill with your own credentials,
    rename it creds.py, and double check to make sure that
    creds.py is in the .gitignore file
"""

import sqlalchemy


def to_url(cred_dict):
    url = sqlalchemy.engine.url.URL(
        'postgres',
        host=cred_dict['host'],
        database=cred_dict['database'],
        username=cred_dict['user'],
        password=cred_dict['password']
    )
    return url


# For connecting to C21U database, see e-mail from Qualtrics
c21u_psql = {
    'host': '',
    'port': 5432,
    'database': '',
    'user': '',
    'password': ''
}

c21u_url = to_url(c21u_psql)

c21u_mongo = {
    'host': '',
    'port': 27017,
    'authSource': 'edx',
    'username': '',
    'password': ''
}

c21u_ec2 = {
    'id': ''
}
