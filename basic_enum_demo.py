# basic_enum_demo.py
# CS 3350 - Programming Languages
# Python side of the Java vs Python enum comparison
#
# Java code we're mirroring:
#
#   public enum DIGIT {
#       ZERO(0),
#       ONE(1),
#       TWO(2),
#       THREE(3),
#       FOUR(4);
#
#       private int val;
#
#       DIGIT(int value) {
#           this.val = value;
#       }
#   }

from enum import Enum

# --- Enum Declaration ---
# Python equivalent of the Java DIGIT enum above
# Instead of a private field + constructor, Python unpacks
# the tuple value directly in __init__ and stores it as self.val

class DIGIT(Enum):
    ZERO  = 0
    ONE   = 1
    TWO   = 2
    THREE = 3
    FOUR  = 4

    def __init__(self, value):
        self.val = value   # mirrors: private int val;  this.val = value;


# --- Variable Assignment & Printing ---
# Java:   DIGIT d = DIGIT.THREE;
#         System.out.println(d);          // THREE
#         System.out.println(d.val);      // won't print (private)
#         System.out.println(d.ordinal()); // 2
#
# Python: d = DIGIT.THREE
#         print(d)        # DIGIT.THREE
#         print(d.val)    # 3  (no access restrictions like Java's private)
#         print(d.name)   # THREE

print("=== Variable Assignment & Printing ===")
d = DIGIT.THREE
print(f"d = DIGIT.THREE")
print(f"  print(d)           -> {d}")
print(f"  d.name             -> {d.name}")
print(f"  d.val              -> {d.val}")
print(f"  d.value            -> {d.value}")
print()
print("  Java note: 'val' is private so you'd need a getter like d.getVal()")
print("  Python has no private enforcement - d.val works directly")
print()


# --- Iterating ---
# Java:   for (DIGIT d : DIGIT.values()) { System.out.println(d + " = " + d.ordinal()); }
# Python: for d in DIGIT: print(d.name, d.val)

print("=== Iterating over DIGIT ===")
for digit in DIGIT:
    print(f"  {digit.name:6s}  val={digit.val}")
print()


# --- Out-of-Range / Beyond Normal Usage ---
# Java:
#   DIGIT bad = (DIGIT) 99;  <-- COMPILE ERROR, not allowed
#   There's no built-in way to get an enum from an int.
#   Java catches this at COMPILE TIME.
#
# Python:
#   DIGIT(99) -- this runs but throws ValueError at RUNTIME
#   Python doesn't know about it until the program actually executes.

print("=== Out-of-Range Integer (Beyond Normal Usage) ===")
print("Trying DIGIT(99)...")
try:
    bad = DIGIT(99)
    print(f"  Got: {bad}")
except ValueError as e:
    print(f"  ValueError: {e}")
    print("  Python: caught at RUNTIME")
    print("  Java:   caught at COMPILE TIME (can't cast int -> enum)")
print()

print("Trying DIGIT(5) - one past our range (we only go to FOUR=4)...")
try:
    bad = DIGIT(5)
    print(f"  Got: {bad}")
except ValueError as e:
    print(f"  ValueError: {e}")
    print("  Same result - Python checks at runtime, Java prevents at compile time")
print()

# what about a valid lookup?
print("Trying DIGIT(2) - this should work (TWO)...")
good = DIGIT(2)
print(f"  DIGIT(2) -> {good.name}, val={good.val}")
print()

# wrong type entirely
print("Trying DIGIT('THREE') - a string instead of int...")
try:
    bad = DIGIT("THREE")
    print(f"  Got: {bad}")
except ValueError as e:
    print(f"  ValueError: {e}")
    print("  Java: DIGIT.valueOf('THREE') works by NAME (this is how Java does it)")
    print("  Python: use DIGIT['THREE'] for name-based lookup instead")
    print(f"  DIGIT['THREE'] -> {DIGIT['THREE'].name}, val={DIGIT['THREE'].val}")
