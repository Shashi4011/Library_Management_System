class LibraryError(Exception):
    pass

class UserAlreadyExists(LibraryError):
    def __init__(self, message ="User already exists"):
        self.message=message
        super().__init__(message)

class UserNotFound(LibraryError):
    def __init__(self, message  ="User not found"):
        self.message=message
        super().__init__(message)

class BookNotFound(LibraryError):
    def __init__(self, message  ="book not found"):
        self.message=message
        super().__init__(message)


class DuplicateBookISBNError (LibraryError):
    def __init__(self, message  =" Duplicate Book ISBN Error "):
        self.message=message
        super().__init__(message)  


class TransactionNotFound (LibraryError):
    def __init__(self, message  =" Transaction Not Found "):
        self.message=message
        super().__init__(message)  

     
     
     
          