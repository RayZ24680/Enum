from enum import Enum

#enum_match_case.py
#CS 3350 - Programming Languages
#tests how python handles exhaustive and non-exhaustive match cases with enums

#define a simple enum
class Test(Enum):
    ONE = 1
    TWO = 2
    THREE = 3

#match case that covers every variant
x = Test.ONE;
match x:
    case Test.ONE:
        print("1")
    case Test.TWO:
        print("2")
    case Test.THREE:
        print("3")

#match case that omits the third case
y = Test.THREE;
match y:
    case Test.ONE:
        print("1")
    case Test.TWO:
        print("2")
#no error, simply exits match case without printing anything
