from library_management.models.book_model import Books
from library_management.database.book_queries import BookQueries
from library_management.utils import execeptions
class BookServices:
    def __init__(self,db_file):
        self.db_file=db_file
        self.book_queries=BookQueries(self.db_file)

    def get_one_book(self,book_id):
        book=self.book_queries.get_book(book_id=book_id)
        if book:
            return book
        else:
            raise execeptions.BookNotFound
        
    def get_all_books(self):
        return self.book_queries.get_all_book()
    

    def add_book(self,title ,author,isbn,available_copies):
        book=Books(title=title,
                   author=author,
                   isbn=isbn,
                   avaliable_copies=available_copies)
        book_id=self.book_queries.add_book(title=book.title,
                                           author=book.author,
                                           isbn=isbn,
                                           available_copies=available_copies)
        if book_id:
            return self.get_one_book(book_id=book_id)
        else:
            raise execeptions.DuplicateBookISBNError 
        
    def update_book(self,book_id,title=None,author=None, isbn=None,available_copies=None):
        book_id=self.book_queries.update_book(book_id=book_id,
                                              title=title,
                                              author=author,
                                              isbn=isbn,
                                              available_copies=available_copies)
        if book_id:
            return self.get_one_book(book_id=book_id)
       
    
    def remove_book(self, book_id):
        book=self.book_queries.update_book(book_id=book_id)
        book_id=self.book_queries.remove_book(book_id=book_id[0])
        return book_id
    
    def is_available(self,book_id):
        book=self.get_one_book(book_id=book_id)
        return book[4]>0
    
    def close_connection(self):
        self.book_queries.close_connection()
