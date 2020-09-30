import mysql.connector
from mysql.connector import Error
import Utilities
import time
import sys
import webbrowser
from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)


CREATE_DATABASE = True
DELETE_DATABASE = True
# info = (host, database_name, user, password) = ('localhost', 'URLs', 'root', '')
# table_name = "URLs"
# localhost = "http://localhost:5000/"


def longURL_to_shortURL(info, longURL, customURL=''):
    # check whether a long link exist
    query = """SELECT * FROM URLs WHERE hash_longURL = %s"""
    values = (Utilities.hash_string(longURL), )
    result = Utilities.execute_database_mysql(info, query, values)

    # if longURL exit, return the shortURL
    if result:
        print("longURL exit. shortURL: " + result[0][3])
        return result[0][3]

    # if longURL does not exist, insert the new longURL and shortURL to table
    else:
        print("longURL does not exit. Add new longURL to database")
        shortURL = localhost + customURL + '_' + str(int((time.time() * 1e6)))
        query = "INSERT INTO URLs (hash_longURL, hash_shortURL, longURL, shortURL) " \
                "VALUE (%s, %s, %s, %s)"
        values = (Utilities.hash_string(longURL), Utilities.hash_string(shortURL), longURL, shortURL)
        result = Utilities.execute_database_mysql(info, query, values, commit=True)
        # print("short link: " + result[3])

        # check whether a short link exist
        query = """SELECT * FROM URLs WHERE hash_shortURL = %s"""
        values = (Utilities.hash_string(shortURL), )
        result = Utilities.execute_database_mysql(info, query, values)
        print("shortURL: " + result[0][3])
        return result[0][3]


def shortURL_to_longURL(info, shortURL):
    # given a short link, search for long link
    query = """SELECT * FROM URLs WHERE hash_shortURL = %s"""
    values = (Utilities.hash_string(shortURL), )
    result = Utilities.execute_database_mysql(info, query, values)
    if result:
        print("longURL: " + result[0][2])
        return result[0][2]
    else:
        print("this shortURL does not exit")
        return None


# # for testing - with a longURL
# longURL = "https://www.w3schools.com/python/python_mysql_create_db.asp"
# shortURL = longURL_to_shortURL(info, longURL)
# longURL = shortURL_to_longURL(info, shortURL)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/longURL', methods=['POST', 'GET'])
def get_longURL():
    if request.method == 'POST':
        result = request.form
        # get longURL and return short URL
        longURL = result['longURL']
        customURL = result['customURL']
        shortURL = longURL_to_shortURL(info, longURL, customURL)
        # result are immutable. We need to make a new dict
        new_result = {
            'longURL': longURL,
            'shortURL': shortURL
        }
        return render_template("longURL.html", result=new_result)


# get short URL and redirect to page
@app.route('/<string:shortURL>', methods=['GET', 'POST'])
def get_shortURL(shortURL):
    longURL = shortURL_to_longURL(info, localhost + shortURL)
    webbrowser.open(longURL)
    # return "redirect to " + longURL
    return ('', 204)  # return empty html
    # return webbrowser.open_new_tab(longURL)


def main():
    global info, host, database_name, user, password, table_name, localhost
    host, database_name, user, password, table_name, localhost = sys.argv[1:]
    info = (host, database_name, user, password)
    print('info: ', info)

    # delete the database
    if DELETE_DATABASE:
        Utilities.delete_database_mysql(info)

    # create a new database
    if CREATE_DATABASE:
        Utilities.create_database_mysql(info)

        # create a table
        query = "CREATE TABLE URLs (" \
                "hash_longURL VARCHAR(255) PRIMARY KEY," \
                "hash_shortURL VARCHAR(255)," \
                "longURL VARCHAR(255)," \
                "shortURL VARCHAR(255))"
        Utilities.execute_database_mysql(info, query)
        query = "SHOW TABLES"
        Utilities.execute_database_mysql(info, query)


if __name__ == '__main__':
    main()
    app.run(debug=False)

