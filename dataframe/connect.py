"""Helper code to quickly connect to our databases."""

import pymongo
import boto3
import creds
import sqlalchemy


def start_instance():
    """Boots the ec2 instance."""
    ec2 = boto3.client('ec2', region_name='us-east-1')
    ec2.start_instances(InstanceIds=[creds.c21u_ec2['id']])
    waiter = ec2.get_waiter('instance_running')
    waiter.wait()


def mongo_client():
    """Connect to mongo client."""
    client = pymongo.MongoClient(
        **creds.c21u_mongo,
        authMechanism='SCRAM-SHA-256',
    )
    return client


def mongo_database(db_name):
    """Connect to mongo database."""
    client = mongo_client()
    return client[db_name]


def get_db():
    start_instance()
    return mongo_database(creds.c21u_mongo['authSource'])


def sql_engine():
    return sqlalchemy.create_engine(creds.c21u_url)
