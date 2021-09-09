import sqlite3

class Sql():

    def __init__(self):
        self.db = sqlite3.connect("./db.db")
        self.c = self.db.cursor()

    def query(self, query):
        return self.c.execute(query)

    def insert(self, query):
        return self.c.execute(*query)

    def close(self):
        self.db.close()

    def commit(self):
        self.db.commit()

sql_instance = Sql()

title ="test"
text = "test"
date="asd"
author ="test"
image ="asd"
filename ="asd"

sql = "INSERT INTO posts(title,text,date,author,image) VALUES (?,?,?,?,?)",(title, text, date, author, filename,)
sql_instance.insert(sql)
sql_instance.commit()

