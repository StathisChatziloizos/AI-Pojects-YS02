class Person:
    def __init__(self, fname, lname, age):
        self.firstName = fname;
        self.lastName = lname;
        self.age = age;
    def print(self):
        print(self.firstName, type(self.firstName))
        print(self.lastName, type(self.lastName))
        print(self.age, type(self.age))

class ID:
    def __init__(self, person, idNumber, birthCity):
        self.person = person
        self.idNumber = idNumber
        self.birthCity = birthCity
    
    def print(self):
        self.person.print()
        print(self.idNumber, type(self.idNumber))
        print(self.birthCity, type(self.birthCity))
        print("------------------")