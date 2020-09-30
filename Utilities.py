import mysql.connector
from mysql.connector import Error
import hashlib


def create_database_mysql(info):
    (host, database_name, user, password) = info
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password)
        cursor = connection.cursor()
        query = "CREATE DATABASE " + database_name
        cursor.execute(query)
        cursor.execute("SHOW DATABASES")
        print(cursor)
        for x in cursor:
            print(x)
        print("Database Created successfully ")
    except mysql.connector.Error as error:
        print("Failed to Delete table and database: {}".format(error))


def delete_database_mysql(info):
    (host, database_name, user, password) = info
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database_name,
            user=user,
            password=password)
        cursor = connection.cursor()

        # delete_table_query = """DROP TABLE Laptop"""
        # cursor.execute(delete_table_query)

        delete_database_query = "DROP DATABASE " + database_name
        cursor.execute(delete_database_query)
        # connection.commit()
        print("Database Deleted successfully ")

    except mysql.connector.Error as error:
        print("Failed to Delete table and database: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def execute_database_mysql(info, query, values=None, commit=False):
    (host, database_name, user, password) = info
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database_name,
            user=user,
            password=password)
        cursor = connection.cursor()
        cursor.execute(query, values)
        if commit:
            connection.commit()
        print('\n')
        print(cursor)
        result = []
        for x in cursor:
            # print(x)
            result.append(x)
        # result = cursor.fetchone()
        # if result:
        #     for x in result:
        #         print(x)
        print("Executed successfully ")
        return result

    except mysql.connector.Error as error:
        print("Failed to connect table and database: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def hash_string(user_string):
    return hashlib.sha256(user_string.encode()).hexdigest()
