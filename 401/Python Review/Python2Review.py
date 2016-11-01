####################################
# whitespace is important
####################################

listOfNumbers = [1, 2, 3, 4, 5, 6]

for number in listOfNumbers:
    print number,
    if (number % 2 == 0):
        print "is even"
    else:
        print "is odd"
        
print "All done now."


####################################
# importing modules
####################################

# install numpy package in Python 2 from command line (Mac, Linux): 
    # sudo pip install -U numpy

    # OR

    # use development enviroment (e.g., Canopy)

import numpy as np

A = np.random.normal(25.0, 5.0, 10)
print A


####################################
# lists
####################################

x = [1, 2, 3, 4, 5, 6]
print len(x)

print x[:3]

print x[3:]

print x[-2:]

x.extend([7,8])
print x

x.append(9)
print x

y = [10, 11, 12]
listOfLists = [x, y]
print listOfLists

print y[1]

z = [3, 2, 1]
z.sort()
print z

z.sort(reverse=True)
print z


####################################
# tuples
####################################

#Tuples are just immutable lists. Use () instead of []

x = (1, 2, 3)
print len(x)

y = (4, 5, 6)
print y[2]

listOfTuples = [x, y]
print listOfTuples

(age, income) = "32,120000".split(',')
print age
print income


####################################
# dictionaries
####################################

# Like a map or hash table in other languages

captains = {}
captains["Enterprise"] = "Kirk"
captains["Enterprise D"] = "Picard"
captains["Deep Space Nine"] = "Sisko"
captains["Voyager"] = "Janeway"

print captains["Voyager"]

print captains.get("Enterprise")

print captains.get("NX-01")

for ship in captains:
    print ship + ": " + captains[ship]
    

####################################
# functions
####################################

def SquareIt(x):
    return x * x
print SquareIt(2)

#You can pass functions around as parameters
def DoSomething(f, x):
    return f(x)

print DoSomething(SquareIt, 3)

#Lambda functions let you inline simple functions
print DoSomething(lambda x: x * x * x, 3)


####################################
# Boolean expressions
####################################

print 1 == 3

print (True or False)

print 1 is 3

if 1 is 3:
    print "How did that happen?"
elif 1 > 3:
    print "Yikes"
else:
    print "All is well with the world"
    

####################################
# looping
####################################

for x in range(10):
    print x,

for x in range(10):
    if (x is 1):
        continue
    if (x > 5):
        break
    print x,
    
x = 0
while (x < 10):
    print x,
    x += 1
    
    