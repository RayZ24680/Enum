from enum import Enum

#enum_iteration.py
# CS 3350 - Programming Languages
#simple iteration through an enum

#define a simple enum
class Test1(Enum):
    ONE = 1
    TWO = 2
    THREE =3

#iterate through with a for loop
for num in Test1:
    print(num)


#same simple enum but with an added alias for the second member
class Test2(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    TWO_ALIAS = 2

#iterate through with a for loop
for num in Test2:
    print(num)

#when iterating, python skips any alias present by default
#can use special attribute __members__ to read aliases
for num, members in Test2.__members__.items():
    print(num)
