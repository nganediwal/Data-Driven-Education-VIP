import os
import psycopg2
import pymongo
import config

conn = psycopg2.connect(
    dbname=config.elephantsql_db,
    user=config.elephantsql_user,
    host=config.elephantsql_host,
    port=config.elephantsql_port,
    password=config.elephantsql_password)

cursor = conn.cursor()
postgreSQL_select_Query = "select * from info"
cursor.execute(postgreSQL_select_Query)
info_records = cursor.fetchall()

# These 2 lines of data prints out everything in the info table as tuples
# for row in info_records:
#     print(row)


#################################################################
client = pymongo.MongoClient("mongodb+srv://%s:%s@%s/%s?retryWrites=true&w=majority" % (config.mongo_user, config.mongo_password, config.mongo_host, config.mongo_db))

mydb = client[config.mongo_db]
mycol = mydb[config.mongo_collection]
mycur = mycol.find({})

# for doc in mycur:
#     print(doc)

#################################################################
def get_student_data_PSQL(student_id):
    postgreSQL_select_Query = "select * from info where user_id = " + str(student_id)
    cursor.execute(postgreSQL_select_Query)
    temp = cursor.fetchall()
    if len(temp) == 0:
        print("No student with that ID was found.")
        # TODO: Raise an exception?
        return ()
    return temp[0]

def get_student_data_mongoDB(student_id):
    mycur = mycol.find({"student_id": student_id})
    if mycol.count_documents({"student_id": student_id}) == 0:
        print("No student with that ID was found.")
        return {}
    return mycur[0]

# print(get_student_data_PSQL(35087))
# print(get_student_data_mongoDB(58294))