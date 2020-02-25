"""Why should you care about python?"""

# Mature super-powerful libraries with backends in C (super fast!)
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
X, y = load_iris(return_X_y=True)
clf = LogisticRegression(random_state=0).fit(X, y)
clf.predict(X[:2, :])
clf.score(X, y)

"""Basic Python Features"""

# Mandatory... string types
print("'Hello World!'")
print('"Hello World!"')
print("Hello \"World\"")
print("""Hello, so-called 'world', aka the "world"!""");
# This is a theme in Python, there's 4-5 ways to do the same thing...
# Note the ; in the last one, ; is entirely optional (python ignores it)

# Different ways, same output...
print("""
Bla blah
""")
print("\nBla blah\n")

# BTW Everything is an object...
help(str)
# Private methods don't exist, just a convention to use __method__ when the
# method should not be used

# Formatting a string
x = 10
print(x)
# The latest!
print(f"I have {x} dogs.")
# The previous one...
print("no, it was {} dogs, or was it {} dogs?".format(x, x-1))
# The OG, python's first and based on Fortran's string formatting
print("or was it %i dogs? Probably more than %10.5i..." % (x, 3))
# When you forget...
print("no, it was "+str(x-5)+" dogs.")

# Lists and loops
my_list = [1, 2, "%x" % x, 10, print]
final_list = []  # Initialize
for i in range(10):
    print(i)
    final_list.append(i)
print(final_list)
my_list = [i for i in range(10)]
my_list = [i*i for i in range(10)]

# apply functions to items in a list
def square(x):
    print(x)
    return x*x
# Happens now, list comprehension
my_list = [square(i) for i in range(10)]
# Happens when needed
my_generator = (square(i) for i in range(10))
print(my_generator)
for item in my_generator:
    print(item)  # This is when we square it
for item in my_list:
    print(item)  # We squared it way back in line 35!
for item in my_generator:
    print(item)  # Nothing happens, we already used up all of the items!
my_map = map(square, range(10))  # Very similar to generator, different syntax

# Simple functions can be defined in-line via a lambda
my_list = list(my_map)  # it's easy to turn a map or generator into a list
my_map_lambda = map(lambda i: i*i, range(10))  
my_list = [i*i for i in range(10)]  # you wouldn't use a lambda here...

"""
Use generators if you have an expensive operation
Use a list comprehension if it's not expensive and you want to use it
multiple times
"""

# Error handling
try:
    x[10] = 10
except TypeError as e:
    print("TypeEe)
    print("Error handling in python!")

# Pandas

import pandas as pd
import numpy as np

np.random.seed(110)
grades = np.random.normal(0.8, 0.2, size=10)
grades[grades > 1] = 1
course_id = [1, 1, 2, 2, 3, 3, 3, 3, 3, 3]
user_id = [1, 2, 1, 2, 1, 2, 3, 4, 5, 6]

def labeler(x):
    """
    This is a docstring, it should describe what this function does.
    """
    if x >= .9:
        return 'A'
    elif (x < .9) and (x >= .8):
        return 'B'
    elif (x < .8) and (x >= .7):
        return 'C'
    elif (x < .7) and (x >= .6):
        return 'D'
    return 'F'

# If you want to learn about a function, try help
help(labeler)
# If help doesn't work, try google
# If google doesn't work, try stackoverflow
# If stackoverflow doesn't work, try me

df = pd.DataFrame({
    'grade': grades,
    'course_id': course_id,
    'user_id': user_id
})

df = df.set_index(['course_id', 'user_id'])
df['label'] = df.grade.apply(labeler)
agg_df = df.groupby('label')['grade'].mean()
agg_df.columns = ['average grade']

"""
How to learn stuff

Try to do a project
If you get stuck, google
If you're still stuck, ask for help
"""
