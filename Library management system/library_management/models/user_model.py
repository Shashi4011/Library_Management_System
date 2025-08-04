class User:
    def __init__(self,name ,email,role):
        self.name=name
        self.email=email
        self.role=role

class Librarian(User):
    def __init__(self, name, email, role="librarian"):
        super().__init__(name, email, role)
class Student(User):
    def __init__(self, name, email, role="student"):
        super().__init__(name, email, role)        