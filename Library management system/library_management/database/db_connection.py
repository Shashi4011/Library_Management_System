import sqlite3
from sqlite3 import Error

class DBConnection:
    def __init__(self,db_file):
        self.db_file=db_file
        self.connection = None

    def connect(self):
        try:
            self.connection =sqlite3.connect(self.db_file)
            self.connection.execute("PRAGMA foregin_keys=ON;")
            print("connected sucessfully")    
        except sqlite3.Error as e:
            print(f"Database error:{e}")
        return self.connection

    def close(self):
        try:
            if self.connection:
                self.connection.close()
                print("connection closed")
        except sqlite3.Error as e:
            print(f"Database error:{e}")


# db=DB_connection("library.db")
# db.connect()
# db.close()