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
    dbname=config.psql_db,
    user=config.psql_user,
    host=config.psql_host,
    port=config.psql_port,
    password=config.psql_password
)
postgres_cursor = postgres_connection.cursor()

# postgres_select_query = """
# SELECT * FROM jiti.dataframe
# """
# postgres_cursor.execute(postgres_select_query)
# postgres_data = postgres_cursor.fetchall()

# These 2 lines of data prints out everything in the info table as tuples
# for row in postgres_data:
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
alchemyEngine = create_engine("postgres+psycopg2://%s:%s@%s:%s/%s" % (config.psql_user, config.psql_password, config.psql_host, config.psql_port, config.psql_db))
postgres_pandas_connection = alchemyEngine.connect()

# dbConnection.close()

#################################################################
# Function: Get specific rows from psql table
# Parameter: value - for a row of data, the column_name of that row needs to equal value
#            column_name (String) - column that is being used to find the correct row(s) of data
#            table (String) - table that holds the data that the model acts on
#            schema (String) - schema within the database that has the table
# Return: An array of arrays where each array is a row from the table that fits the query
def get_student_data_PSQL(value, column_name, table, schema = 'jiti'):
    psql_select_query = "SELECT * FROM %s.%s WHERE %s = %s" % (schema, table, column_name, value)
    postgres_cursor.execute(psql_select_query)
    returned_data = postgres_cursor.fetchall()
    if len(returned_data) == 0:
        print("No student with that ID was found.")
        # TODO: Raise an exception?
        return ()
    return returned_data

# Function: Get the column names of a table within psql
# Parameter: table (String) - table to get the column names for
#            schema (String) - schema that has the table within the database
# Return: An array with the column names of the table
def get_column_names_PSQL(table, schema = 'jiti'):
    psql_select_query = "SELECT * FROM %s.%s LIMIT 0" % (schema, table)
    postgres_cursor.execute(psql_select_query)
    colnames = [desc[0] for desc in postgres_cursor.description]
    del colnames[0]
    return colnames

# Function: Get dict of student data from mongo
# Parameter: student_id (integer) - id of the student to get a dict of data for
# Return: A dict of the data of a student with id = student_id
def get_student_data_mongoDB(student_id):
    if mongo_collection.count_documents({"student_id": student_id}) == 0:
        print("No student with that ID was found.")
        # TODO: Raise an exception?
        return {}
    mycursor = mongo_collection.find({"student_id": student_id})
    # TODO: make this function return as tuple rather than dict (to match postgres)
    return mycursor[0]

# Function: Returns all the data within a table as a dataframe
# Parameter: table (String) - table that holds the data to be put in a dataframe
#            schema (String) - schema that has the table
#            index_column (String) - column from psql that is to be set as the index column
#                                    in the dataframe (not really needed)
# Return: A dataframe with all the data from the table
def export_data_to_df(table, schema = 'jiti', index_column = None):
    postgresdf = pd.read_sql("SELECT * FROM %s.%s" % (schema, table), postgres_pandas_connection, index_col=index_column)
    return postgresdf

# Function: Applies weights to certain columns of a row of data (to act like a data model)
# Parameter: file_name (String) - csv file that holds the weights of the data.  The csv file should be
#                                 in the temp_model folder, which is the same directory as this studentdata.py file.  
#                                 file_name should end with '.csv'
#            value - for a row of data, the column_name of that row needs to equal value
#            column_name (String) - column that is being used to find the correct row(s) of data
#            table (String) - table that holds the data that the model acts on
#            schema (String) - schema within the database that has the table
# Return: A single value that is the dot product between the attributes of data and their respective weights
def dummy_model_postgres(file_name, value, column_name, table, schema = 'jiti'):
    # TODO: student_data needs to be aggregated properly instead of getting the 0 index of the returned array
    # TODO: take in a parameter of array of column names to apply weights to
    student_data = np.asarray(get_student_data_PSQL(value, column_name, table, schema)[0][4:11])
    weights = []
    with open('./temp_model/' + file_name) as weightsfile:
        weights = [float(s) for line in weightsfile.readlines() for s in line[:-1].split(',')]
    return np.dot(student_data, weights)
#################################################################

# Example of how to properly call functions:

COLUMNNAMES = get_column_names_PSQL('dataframe')
# print(COLUMNNAMES)

# print(get_student_data_PSQL(3013850, 'user_id', 'dataframe'))
# print(get_student_data_mongoDB(58294))
# print(export_data_to_df('dataframe'))
# print(dummy_model_postgres('dummy_weights.csv', 3013850, 'user_id', 'dataframe'))