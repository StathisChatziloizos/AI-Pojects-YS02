class Person:
    counter = 0

    def __init__(self, firstName=None, lastName=None, age=None):
        Person.counter += 1
        self.firstName = firstName
        self.lastName = lastName
        self.age = age

        if lastName is None:
                self.compare(firstName)

    def print(self):
        print("First Name: " + self.firstName)
        print("Last Name: " + self.lastName)
        print("Age: " + str(self.age))

    def classData(self):
        print("Counter: ", str(self.counter))

    def compare(self, other):
        self.firstName = other.firstName
        self.lastName = other.lastName
        self.age = other.age


p1 = Person("Stathis", "Chatziloizos", 21)
p2 = Person(p1)
p1.print()
p2.print()
p1.classData()