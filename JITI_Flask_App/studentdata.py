import os
import csv
import psycopg2
import pymongo
import config
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# create postgres connection
postgres_connection = psycopg2.connect(
    dbname=config.elephantsql_db,
    user=config.elephantsql_user,
    host=config.elephantsql_host,
    port=config.elephantsql_port,
    password=config.elephantsql_password
)

postgres_cursor = postgres_connection.cursor()
postgres_select_query = "select * from info"
postgres_cursor.execute(postgres_select_query)
postgres_info_records = postgres_cursor.fetchall()

# These 2 lines of data prints out everything in the info table as tuples
# for row in info_records:
#     print(row)


#################################################################

# create mongo connection
mongo_client = pymongo.MongoClient("mongodb+srv://%s:%s@%s/%s?retryWrites=true&w=majority" % (config.mongo_user, config.mongo_password, config.mongo_host, config.mongo_db))

mongo_db = mongo_client[config.mongo_db]
mongo_collection = mongo_db[config.mongo_collection]
mongo_cursor = mongo_collection.find({})

# for doc in mycur:
#     print(doc)


#################################################################

# simplify taking data from a table in psql and turn it into df using sqlalchemy
alchemyEngine = create_engine("postgres+psycopg2://%s:%s@%s:%s/%s" % (config.elephantsql_user, config.elephantsql_password, config.elephantsql_host, config.elephantsql_port, config.elephantsql_db))

postgres_pandas_connection = alchemyEngine.connect()

# dbConnection.close()

#################################################################
# this function takes in id and returns a tuple for the row that has that id
def get_student_data_PSQL(id):
    postgreSQL_select_Query = "select * from info where id = " + str(id)
    postgres_cursor.execute(postgreSQL_select_Query)
    returned_data = postgres_cursor.fetchall()
    if len(returned_data) == 0:
        print("No student with that ID was found.")
        # TODO: Raise an exception?
        return ()
    return returned_data[0]


def get_column_names_PSQL():
    postgres_cursor.execute("Select * from info LIMIT 0")
    colnames = [desc[0] for desc in postgres_cursor.description]
    return colnames

# TODO: make this function return as tuple rather than dict (to match postgres)
# this function takes in a student_id and returns the dict for the student with that id
def get_student_data_mongoDB(student_id):
    if mongo_collection.count_documents({"student_id": student_id}) == 0:
        print("No student with that ID was found.")
        # TODO: Raise an exception?
        return {}
    mycursor = mongo_collection.find({"student_id": student_id})
    return mycursor[0]

# this function takes in a table name (string) and index_column name (string) and returns data in table from postgres as dataframe
def export_data_to_df(table, index_column = None):
    postgresdf = pd.read_sql("SELECT * FROM " + table, postgres_pandas_connection, index_col=index_column)
    return postgresdf

# TODO: avoid hardcoding file_name, elements of tuple returned by get_student_data_PSQL
# this function takes in a file_name (String, should be csv and stored in ./temp_model) and id and return the dot product of some of id's fields and the weights
def dummy_model_postgres(file_name, id):
    student_data = np.asarray(get_student_data_PSQL(id)[4:11])
    weights = []
    with open('./temp_model/dummy_weights.csv') as weightsfile:
        weights = [float(s) for line in weightsfile.readlines() for s in line[:-1].split(',')]
    return np.dot(student_data, weights)
    
COLUMNNAMES = get_column_names_PSQL()

# print(get_student_data_PSQL(18))
# print(get_student_data_mongoDB(58294))
# print(export_data_to_df('info', 'id')) info is name of table, id is id column from the csv Jonna sent us
# print(dummy_model_postgres(None, 18))