import sqlite3
from library_management.database.db_connection import DBConnection

class TransactionQueries:
    def __init__(self,db_file):
        self.db_file= db_file
        self.db=DBConnection(self.db_file)
        self.connection =self.db.connect()
        self.cursor =self.connection.cursor()
        self.create_table()

    def create_table(self):
        create_table_query ="""
        CREATE TABLE IF NOT EXISTS transactions( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        book_id INTEGER NOT NULL,
        borrowed_date TEXT  NOT NULL,
        returned_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
        FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE CASCADE
        );
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print('transaction table created!')

    def borrow_book(self,user_id,book_id,borrowed_date):
        try:
            borrow_query="""
            INSERT INTO transactions (user_id,book_id,borrowed_date) VALUES (?,?,?);
            """
            self.cursor.execute(borrow_query,(user_id,book_id,borrowed_date))
            self.connection.commit()
            transaction_id=self.cursor.lastrowid

            update_query="""
            UPDATE books SET available_copies= available_copies -1 WHERE id=?;
            """
            self.cursor.execute(update_query,(book_id,))
            self.connection.commit()
            print(f"Books ID :{book_id} borrowed by :{user_id} with transaction ID:{transaction_id}")
            return transaction_id
        except sqlite3.Error as e:
            print(f"Database Error:{e}")

    def return_book(self,transaction_id,returned_date):
        try:
            transaction=self.get_transaction_by_id(transaction_id)
            book_id=transaction[2]
            return_query="""
            UPDATE transactions SET returned_date =? WHERE id=?; 
            """
            self.cursor.execute(return_query,(returned_date,transaction_id))
            self.connection.commit()
                
            update_query="""
            UPDATE books SET available_copies=available_copies+1 WHERE id=?;
            """
            self.cursor.execute(update_query,(book_id,))
            self.connection.commit()
            print(f"Book with ID {book_id} returned on {returned_date}")
            return book_id,returned_date
        except sqlite3.Error as e:
            print(f"Database Error:{e}")

    def get_transaction_by_id(self,transaction_id):
        select_query="""
        SELECT *  FROM transactions WHERE id=?;
        """
        self.cursor.execute(select_query,(transaction_id,))
        transaction=self.cursor.fetchone()
        print(transaction)
        return transaction
    
    def get_transaction_by_user_id(self,user_id):
        select_query="""
        SELECT * FROM transactions WHERE user_id=?;
        """
        self.cursor.execute(select_query,(user_id,))
        transactions=self.cursor.fetchall()
        print(transactions)
        return transactions     

    def close_connection(self):
        self.db.close()

# transaction_queries=TransactionQueries("library.db")
# transaction_queries.borrow_book('STDJ01',2,"2025-03-22")
# transaction_queries.borrow_book('STDJ02',3,"2025-3-22")
# transaction_queries.get_transaction_by_id(2)
# transaction_queries.return_book(2, '2025-3-22')
# transaction_queries.get_transaction_by_user_id(2)
# transaction_queries.get_transaction_by_user_id('STDJ61')
# transaction_queries.close_connection()

