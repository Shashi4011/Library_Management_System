from library_management.services.user_services import UserServices
from library_management.services.book_service import BookServices
from library_management.services.transaction_service import TransactionServices
from library_management.utils import execeptions
from library_management.animations import loader,dot_loader

# can be utilized while registring the librarian
ADMIN_PASS='libraryAdmin@123'

# Database file name 
DB_NAME='library.db'

def establish_connection():
    global user_services ,book_services, transaction_services
    user_services= UserServices(DB_NAME)
    book_services=BookServices(DB_NAME)
    transaction_services=TransactionServices(DB_NAME)

def break_connection():
    user_services.close_connection()
    book_services.close_connection()
    transaction_services.close_connection()

def main_menu():
    print("1. Register User")
    print("2. Manage Book (Librarian Only)")
    print("3. Borrow Book (Student Only)")
    print("4. Return book")
    print("5. View All Books")
    print("6. View Transaction Details By ID")
    print("7. View Transaction Details By User ID")
    print("8. Exit")
    choice=input("Please select an option:")
    return choice


def user_registration():
    print("\n 1. Libraian (Only Admin)" )
    print('2. Student')
    user_type= input('choose your user type:')
    try:
        if user_type=='1':
            admin_pass=input('Enter Admin Password:')
            if admin_pass==ADMIN_PASS:
                name=input('Enter Name:').title()
                email=input('Enter Email:').lower()
                user_id=user_services.register_librarian(name=name,
                                                         email=email)
                print(f"Library'{name}' has been registered with ID:{user_id}")
            else:
                print('Incorrect password try again!')
        elif user_type=='2':
            name=input('Enter Name:').title()
            email=input('Enter Email:').lower()
            user_id=user_services.register_librarian(name=name,
                                                            email=email)
            print(f"student'{name}' has been registered with ID:{user_id}")
        else:
            print('Invalid choice')
    except execeptions.UserAlreadyExists as e:
        print(f"Error:{e}")


def manage_book():
    librarian_id=input("Enter your librarian user ID:").upper()
    try:
        if user_services.is_librarian(user_id=librarian_id):
            print("1. Add Book")
            print("2. Update Book")
            print("3. Remove Book")
            choice= input("Enter your choice:")
            if choice=='1':
                title=input("Enter your title:")
                author=input("Enter author name:")
                isbn=input("Enter isbn:")
                available_copies=input("Enter available_copies:")
                try:
                    book=book_services.add_book(
                        title=title,
                        author=author,
                        isbn=isbn,
                        available_copies=int(available_copies)
                    )
                    print(f"Book'{title}' added with ID:{book[0]}")
                except ValueError as e:
                    print(f"Error:{e}")
                except execeptions.DuplicateBookISBNError as e:
                    print(f"Error:{e}")
            elif choice=='2':
                book_id =input("Enter book ID:")
                try:
                    book=book_services.get_one_book(book_id=book_id)
                    title=input("Enter book title (leave it to keep unchanged):") or None
                    author=input("Enter author name(leave it to keep unchange ):") or None 
                    isbn=input("Enter isbn (leave it to keep unchange ):")or None
                    available_copies=input("Enter available_copies:")
                    available_copies=int(available_copies)if available_copies else None
                    book=book_services.update_book(book_id=book_id,
                                                   title=title,
                                                   author=author,
                                                   isbn=isbn,
                                                   available_copies=available_copies) 
                    if book:
                        print(f"Book ID :{book_id} has been updated!!")
                    else:
                        print("NO fields provided to update")
                except ValueError as e:
                    print(f"Error:{e}")
                except execeptions.BookNotFound as e:
                    print(f'Error:{e}') 
            elif choice =='3':
                try:
                    book_id =int(input("Enter book ID:"))
                    book=book_services.get_one_book(book_id=4)
                    book_services.remove_book(book_id=book_id)
                    print(f"Book ID:{book_id} has been removed!!!")
                except ValueError as e:
                    print(f"Error:{e}")
                except execeptions.BookNotFound as e:
                    print(f'Error:{e}') 
            else:
                print(f'Error:{e}')
        else:
            print("you are not allowed here !!!")

    except execeptions.UserNotFound as e:
        print(f"Error:{e}")




def borrow_book_ui():
    student_id=input("Enter your student user ID:").upper()
    try:
        if user_services.is_student(user_id=student_id):
            book_id=int(input("Enter book iD to borrow:"))
            if book_services.is_available(book_id-book_id):
                book = book_services.get_one_book(book_id=book_id)
                transactions = transaction_services.get_transaction_by_user_id(user_id=student_id)
                if transactions:
                    for transaction in transactions:
                        if book_id == transaction[2]:
                            if not transaction_services.is_returned(transaction_id=transaction[0]):
                                print(f"You have already borrowed '(book[1])' book")
                                return
                    else:
                        transaction_id = transaction_services.borrow_book(
                            user_id=student_id,
                            book_id=book_id)
                    print(f"Book'{book[1]}' successfully borrowed by '{student_id}' with transaction ID:{transaction_id}")
                else:
                    transaction_id=transaction_services.borrow_book(
                        user_id=student_id,
                        book_id=book_id
                    )
                    print(f"Book'{Book[1]}' successfully borrowed by '{student_id}' with transaction ID:{transaction_id}")
            else:
                print("Book is out of stock!!!")

        else:
            print(f"Only students can borrow the book!!!")
    except execeptions.UserNotFound as e:
        print(f"Error {e}")
    except execeptions.BookNotFound as e:
        print(f"Error:{e}")

def return_book_ui():
    try:
        trasaction_id=int(input("Enter transaction id to return the book:"))
        if not transaction_services.is_returned(transaction_id=trasaction_id):
            returned_transaction=transaction_services.return_book(transaction_id=trasaction_id)
            book=book_services.get_one_book(book_id=returned_transaction[0])
            print(f"book '{book[1]}'returned on '{returned_transaction[1]}")
        else:
            print('Book already returned ')
    except ValueError as e:
        print(f'Error:{e}')
    except execeptions.TransactionNotFound as e:
        print(f'Error:{e}')



def display_books():
    try:
        books=book_services.get_all_books()
        if books:
            print("BOOK ID\t TITLE\t BOOK AUTHOR\tISBN\tAVAILABLE COPIES")
            print("------------------------------------------------------")
            for book in books:
                print(f"{book[0]}\t{book[1]}\t{book[2]}\t{book[3]}\t{book[4]}")
        else:
            print("OOPs!,Library does not have any book! Visit Again!")
    except execeptions.BookNotFound as e:
        print(f"Error:{e}")


def display_transaction_by_id():
    """"Displays all transaction details using ID"""
    try:
        transaction_id=int(input("Enter transaction ID to see the details: "))
        transaction=transaction_services.get_transaction_by_id(transaction_id)
        if transaction:
            col_widths = [ 
                max(len(str(transaction[0])), len("TRANSACTION ID")),# TRANSACTION ID
                max(len(str(transaction[1])), len("USER ID")),# USER ID
                max(len(str(transaction[2])), len("BOOK ID")),# BOOK ID
                max(len(str(transaction[3])), len ("BORROWED DATE")) , # BORROWED DATE
                max(len(str(transaction[4])) if transaction[4] else len ("Not returned"), len("RETURNED DATE"))
                ]
# Print header with dynamic spacing
            print(
                f"{'TRANSACTION ID'.ljust(col_widths[0])}"
                f"{'USER ID'.ljust(col_widths[1])}"
                f"{'BOOK ID'.ljust(col_widths[2])}"
                f"{'BORROWED ID'.ljust(col_widths[3])}"
                f"{'RETURNED ID'.ljust(col_widths[4])}"
            )
            print("-"*(sum(col_widths)+8))
            for transation in transaction:
                returned_date=transation[3] if transation[3] else "not returned"
                print(

                )



        


def main():
    print("---Welcome to the Library HUB---")
    print("Establishing connection")
    establish_connection()
    while True:
        choice=main_menu()
        if choice=="1":
            user_registration()
        elif choice=="2":
            manage_book()
        elif choice=="3":
            borrow_book_ui()
        elif choice=="4":
            return_book_ui()
        elif choice=="5":
            display_books()
        elif choice=="8":
            print("closing connection")
            break_connection()
            print("Thank You! Visit Again")
            break

# def  main():
if __name__=="__main__":
     main()







# user_services = UserServices( 'library.db')
# try:
#     print('ID', user_services.register_librarian('shashi','shashi@gmail.com'))
# except execeptions.UserAlreadyExists as e:
#     print(f'error:{e}')
# user_services.close_connection()

# user_services = UserServices( 'library.db')
# try:
#     print('ID', user_services.register_librarian('zoya','z@gmail.com'))
# except execeptions.UserAlreadyExists as e:
#     print(f"Error:{e}")
#     user_services.close_connection()

# user_services = UserServices('library.db')
# try:
#     print('User Data', user_services.get_user(user_id='LBZO04'))
# except execeptions.UserNotFound as e:
#     print(f' Error: {e}')
# user_services.close_connection()

# User_Services=UserServices('library.db')
# try:
#     print(User_Services.is_student('LBZO04'))
# except execeptions.UserAlreadyExists as e:
#     print(f"error:{e}")
# User_Services.close_connection()

# User_Services=UserServices('library.db')
# try:
#     print(User_Services.is_librarian('LBZO04'))
# except execeptions.UserAlreadyExists as e:
#     print(f"error:{e}")
# User_Services.close_connection()


# book_Services=BookServices('library.db')
# try:
#     print(book_Services.get_all_books())
# except execeptions.BookNotFound as e:
#     print(f"error:{e}")
# book_Services.close_connection()


# book_Services=BookServices('library.db')
# try:
#     print(book_Services.add_book('python killer','shashi',1732634747478,1))
# except execeptions.DuplicateBookISBNError as e:
#     print(f"error:{e}")
# book_Services.close_connection()

# book_Services=BookServices('library.db')
# try:
#     book=book_Services.get_one_book(book_id='4')
#     book=book_Services.update_book(book[0],author='bittu')
#     if book:
#         print(book)
#     else:
#         print('not provided any fields to update ')

# except execeptions.BookNotFound as e:
#     print(f"error:{e}")
# book_Services.close_connection()
######################################################################################

# book_Services=BookServices('library.db')
# try:
#     book=book_Services.get_one_book(book_id=4)
#     print(book_Services.remove_book(book_id=book[1]))
# except execeptions.BookNotFound as e:
#     print(f"error:{e}")
# book_Services.close_connection()


######################################################################################
# book_services = BookServices('library.db')
# try:
#     print(book_services.is_available(2))
# except execeptions.BookNotFound as e:
#     print (f'Error: {e}')
# book_services.close_connection()



# transaction_services = TransactionServices ('library.db')
# try:
#     print(transaction_services.get_transaction_by_id(5))
# except execeptions.TransactionNotFound as e:
#     print(f' Error: {e}')
# transaction_services.close_connection()



# transaction_services = TransactionServices(' library.db')
# try:
#     print(transaction_services.get_transaction_by_user_id('STDJ01'))
# except execeptions.UserNotFound as e:
#     print(f' Error: {e}')
# transaction_services.close_connection()



# transaction_services=TransactionServices('library.db')
# try:
#     print(transaction_services.borrow_book(user_id='STZO03',book_id=2))
# except execeptions.UserNotFound as e:
#     print(f'error:{e}')
# except execeptions.BookNotFound as e:
#     print(f'error:{e}')
# transaction_services.close_connection()

# transaction_services=TransactionServices('library.db')
# try:
#     print(transaction_services.return_book(user_id='STZO03',book_id=2))
# except execeptions.BookNotFound as e:
#     print(f'error:{e}')
# transaction_services.close_connection()


def borrow_book_ui(self):
    transaction_services=TransactionServices('library.db')
    try:
        user_id='STPY02'
        book_id=2
        transactions=transaction_services.get_transaction_by_user_id(user_id=user_id)
        for transaction in transactions:
            if book_id== transaction[2]:
                if not transaction_services.is_returned(transaction_id=transaction[0]):
                    print('you have already borrowed the book')
                    return
        print(transaction_services.borrow_book(
            user_id=user_id,
            book_id=book_id
        ))
    except execeptions.UserNotFound as e:
        print(f'Error:{e}')
    except execeptions.BookNotFound as e:
        print(f'Error:{e}')

    transaction_services.close_connection()

# borrow_book_ui()

transaction_services=TransactionServices('library.db')
try:
    if not transaction_services.is_returned(4):
        print(transaction_services.return_book(4))
    else:
        print('book already returned')
except ValueError as e:
    print(f'Error:{e}')
except execeptions.TransactionNotFound as e:
    print(f'Error:{e}')
transaction_services.close_connection()






