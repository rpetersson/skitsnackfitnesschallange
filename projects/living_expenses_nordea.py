# 1 - Take EXCEL file from Nordea and convert it to csv.
# 2 - Store the data in a database.
# 3 - Display data analysis on a page in python.

#Imports
import sqlite3
import pandas as pd
import sys

# PATH TO DATABASE

database = ".\\project_database.db"

# SQLITE TO CREATE DATABASE AND TABLES.

create_table_sql = """

CREATE TABLE IF NOT EXISTS robban_nordea (
 id integer PRIMARY KEY,
 date text,
 name text,
 expense_amount text,
 income_amount text
);


"""

def create_connection(db_file):
    try:
        connect = sqlite3.connect(db_file)
        return connect
    except Exception as e:
        print(e, 1)
        return None

def create_table(connect, create_table_sql):
    try:
        c = connect.cursor()
        c.execute(create_table_sql)

    except Exception as e:
        print(e, 2)


def get_csv_from_dir():

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.max_colwidth', -1)

    pd_excel = pd.read_excel(".\\nordea_testfil.xls","Bevegelser",)


    return pd_excel.head()





def main():
    connect = create_connection(database)

    if connect is not None:
        create_table(connect, create_table_sql)
    else:
        print("Error! connot create the database connection.")

    print(get_csv_from_dir())

if __name__ == '__main__':
    main()