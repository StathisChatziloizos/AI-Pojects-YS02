import sys

""" Run: python3.6 parentheses.py "{inputString}" """


# Check for valid arguments
if len(sys.argv) != 2:
    print("You must give an input string as an argument!")
    print("Example: parentheses.py \"{{()}[]}()\"\n")
    exit(-1)

else:
    input = sys.argv[1]
    print("Input string:", input)



# Stack implementation using python lists
class Stack:
    # Initialize a stack using a list
    def __init__(self):
        self.list = []

    # Check if the stack is empty
    def empty(self):
        if self.list:
            return False
        else:
            return True

    # push data to the top of the stack
    def push(self, data):
        # Data gets inserted to the head of the list
        self.list.insert(0,data)

    # pop the top element from the stack
    def pop(self):
        # Pops the first element of the list
        return self.list.pop(0)
    
    # prints the contents of the stack (top to bottom)
    def print(self):
        for item in self.list:
            print(item, end = '')
        print("\n---------------")


# List of valid characters - Brackets, SQ Brackets, Curly Brackets
validChars = ['(', ')', '[', ']', '{', '}']


# Initialize the Stack
parenthesesStack = Stack()

# Loop through every character of the input string
for char in input:

    # If the character isn't a bracket, then we can ignore it
    if char not in validChars:
        continue

    # If its an opening bracket then push it to the Stack
    if char == '(' or char == '[' or char == '{':
        parenthesesStack.push(char)
        continue

    # At this point char is a closing bracket and if the Stack is empty, then
    # this bracket doesn't have a matching opening bracket, therefore the input isn't balanced
    if parenthesesStack.empty():
        print("Input string is NOT Balanced!")
        exit()
    
    # If char is a closing bracket then the popped character must be the matching
    # opening bracket of char
    if char == ')':
        if parenthesesStack.pop() != '(':
            print("Input string is NOT Balanced!")
            exit()
    
    if char == ']':
        if parenthesesStack.pop() != '[':
            print("Input string is NOT Balanced!")
            exit()
    
    if char == '}':
        if parenthesesStack.pop() != '{':
            print("Input string is NOT Balanced!")
            exit()


# If the stack is not empty, then an opening bracket doesn't have a matching
# closing bracket
if parenthesesStack.empty():
    print("Input string is Balanced!")
else:
    print("Input string is NOT Balanced!")