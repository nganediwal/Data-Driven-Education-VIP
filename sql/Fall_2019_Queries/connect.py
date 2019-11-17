import pymongo
import boto3
import creds


def start_instance():
    """Boots the ec2 instance."""
    ec2 = boto3.client('ec2', region_name='us-east-1')
    ec2.start_instances(InstanceIds=[creds.c21u_ec2['id']])
    waiter = ec2.get_waiter('instance_running')
    waiter.wait()

creds_dict = {
    'forum': creds.c21u_mongo,
    'clickstream': creds.c21u_mongo_clickstream
}

def mongo_client(collection):
    """Connect to mongo client."""
    if collection in creds_dict.keys():
        client = pymongo.MongoClient(
            **creds_dict[collection],
            authMechanism='SCRAM-SHA-256',
        )
        return client
    else:
        raise Exception(collection + ' is not a valid collection!')


def mongo_database(db_name, collection):
    """Connect to mongo database."""
    client = mongo_client(collection)
    return client[db_name]


def get_db(collection):
    start_instance()
    return mongo_database(creds.c21u_mongo['authSource'], collection)
