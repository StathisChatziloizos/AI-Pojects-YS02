fname = "Stathis"
lname = 'Chatziloizos'

fullname = fname + " " + lname;

def find_banana(m_fruits):
    i=0
    for fruit in m_fruits:
        i+=1
        if(fruit == "banana"):
            print("(",i,") Found the banana")
        else:
            print("(",i,") Did not find the banana")

print(fullname);

fruits = ["tangerine","banana", "apple", "orange", "pear", "kiwi", "mango", "pineapple"]
fruits.append("banana")
find_banana(fruits);

print(fruits.pop())
print(fruits.pop())
print(fruits.pop(0))
