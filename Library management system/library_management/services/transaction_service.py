from library_management.models.transaction_model import Transactions
from library_management.database.transaction_queries import TransactionQueries
from library_management.utils import execeptions
from datetime import datetime

class TransactionServices:
    def __init__(self,db_file):
        self.db_file=db_file
        self.transaction_queries=TransactionQueries(self.db_file)

    def get_transaction_by_id(self,transaction_id):
        transaction=self.transaction_queries.get_transaction_by_id(transaction_id=transaction_id)
        if transaction:
            return transaction
        else:
            raise execeptions.TransactionNotFound
        
    def get_transaction_by_user_id(self,user_id):
        transactions=self.transaction_queries.get_transaction_by_user_id(user_id=user_id)
        if transactions:
            return transactions
        
    def borrow_book(self, user_id, book_id):
        borrowed_transaction = Transactions(user_id=user_id,
                                           book_id=book_id,
                                           borrowed_data=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))
        transaction_id=self.transaction_queries.borrow_book(
            user_id=borrowed_transaction.user_id,
            book_id=borrowed_transaction.book_id,
            borrowed_date=borrowed_transaction.borrowed_data
        )
        if transaction_id:
            return transaction_id
        

    def return_book(self,transaction_id):
        returned_transaction=self.transaction_queries.return_book(
            transaction_id=transaction_id,
            returned_date=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))
        if returned_transaction:
            return returned_transaction
        
    def is_returned(self,transaction_id):
        transaction=self.get_transaction_by_id(transaction_id=transaction_id)
        if transaction[4]:
            return True

    def close_connection(self):
        self.transaction_queries.close_connection()