import sqlite3
from library_management.database.db_connection import DBConnection

class UserQueries:
    def __init__(self,db_file):
        self.db_file =db_file
        self.db =DBConnection(self.db_file)
        self.connection = self.db.connect()
        self.cursor =self.connection.cursor()
        self.create_table()

    def create_table(self):
        create_table_query ="""
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL,
        user_id TEXT UNIQUE
        );
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print('user table created!')


    def generate_user_id(self,id,username,role):
        role_prefix='ST' if role.lower() == 'student' else 'LB'
        user_char=username[:2].upper()
        row_id=f"{id:02d}"
        return f"{role_prefix}{user_char}{row_id}"

    def add_user(self, username ,email, role):
        try:
            insert_query ="""
            INSERT INTO users (name, email, role) values(?,?,?);
            """
            self.cursor.execute(insert_query,(username, email, role))
            self.connection.commit()
            id=self.cursor.lastrowid
            generate_user_id=self.generate_user_id(id, username,role)
            update_query="""
            UPDATE users SET user_id =? WHERE id=?;
            """
            self.cursor.execute(update_query,(generate_user_id,id))
            self.connection.commit()
            print(f"Data added and the user ID is :{generate_user_id}")
            return generate_user_id
        except sqlite3.Error as e:
            print(f"Database error:{e}")


    def get_user_by_id(self,user_id):
        select_query="""
        SELECT * FROM users WHERE user_id =?
        """
        self.cursor.execute(select_query,(user_id,))
        user=self.cursor.fetchone()
        # print(user)
        return user
    def close_connection(self):
        self.db.close()


# user_queries=UserQueries("library.db")
# user_queries.add_user('django','d@gmail.com','student')
# user_queries.add_user('python','p@gmail.com','student')
# user_queries.get_user_by_id('STPY08')
# user_queries.close_connection()        