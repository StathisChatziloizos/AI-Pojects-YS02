from random import randrange
import os

os.system("clear")



class Node:
    def __init__(self, data = None, next = None):
        self.data = data
        self.next = next
    
    def print(self):
        print(self.data)

class List:
    def __init__(self):
        self.head = None
    
    def insertNode(self, node):
        if self.head == None:
            self.head = node

        else:
            current = self.head

            while current.next != None:
                current = current.next
            current.next = node
    def insertData(self, data):
        node = Node(data)
        self.insertNode(node)

    def popData(self, data):
        if self.head == None:
            return None

        elif self.head.data == data:
            self.head = self.head.next

        else:
            current = self.head
            previous = current

            while current != None:
                if current.data != data:
                    previous = current
                    current = current.next

                else:
                    previous.next = current.next
                    return current

            return None


    def print(self):
        if self.head == None:
            print("List is empty")

        else:
            counter = 0
            current = self.head
            while current != None:
                counter += 1
                print("(%d)"%(counter), end = "--> ")
                current.print()
                current = current.next

myList = List()
myList.insertData(78)
myList.insertData(7)
myList.print()