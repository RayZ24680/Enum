# enum_match_demo.py
# CS 3350 - Programming Languages
# Demo: match/case with enums -- full coverage vs missing cases
#
# Java equivalent uses switch statements:
#
#   switch (d) {
#       case ZERO:  System.out.println("zero");  break;
#       case ONE:   System.out.println("one");   break;
#       ...
#       default:    System.out.println("unknown"); break;
#   }
#
# Python 3.10+ uses match/case instead

from enum import Enum


class DIGIT(Enum):
    ZERO  = 0
    ONE   = 1
    TWO   = 2
    THREE = 3
    FOUR  = 4


# ============================================================
# PART 1: All cases covered
# Java: every case in the switch is handled
# Python: every member has a matching case branch
# ============================================================

def describe_digit_full(d):
    """match statement with ALL cases covered"""
    match d:
        case DIGIT.ZERO:
            return "zero - nada, nothing, zilch"
        case DIGIT.ONE:
            return "one - the loneliest number"
        case DIGIT.TWO:
            return "two - it takes two to tango"
        case DIGIT.THREE:
            return "three - magic number"
        case DIGIT.FOUR:
            return "four - four-leaf clover"
        case _:
            # this is like Java's 'default' -- catches anything else
            return "unknown digit"


# ============================================================
# PART 2: Missing cases (ZERO and THREE deliberately left out)
# Java: with switch expressions (Java 14+) -- missing cases
#       cause a COMPILE ERROR if there's no default.
#       With old switch statements, it just falls through silently.
# Python: missing cases just fall through to _ (default) or
#         return None silently if there's no default at all
# ============================================================

def describe_digit_missing(d):
    """match statement with ZERO (0) and THREE (3) left out -- on purpose"""
    match d:
        # ZERO is missing
        case DIGIT.ONE:
            return "one"
        case DIGIT.TWO:
            return "two"
        # THREE is missing
        case DIGIT.FOUR:
            return "four"
        # no wildcard _ either -- what happens for ZERO and THREE?


def describe_digit_missing_with_default(d):
    """same missing cases but WITH a default wildcard"""
    match d:
        # ZERO is missing
        case DIGIT.ONE:
            return "one"
        case DIGIT.TWO:
            return "two"
        # THREE is missing
        case DIGIT.FOUR:
            return "four"
        case _:
            # Python silently lands here for ZERO and THREE
            # Java (old switch): falls through with no output
            # Java (switch expression, Java 14+): compile error without default
            return f"[UNHANDLED] {d.name} was not in the match statement!"


# ============================================================
# PART 3: New variant added WITHOUT updating the match
# We add FIVE = 5 to DIGIT after the functions are already written
# and see what happens when we pass it in
# ============================================================

# adding a new member is actually not possible on a frozen enum class,
# so we redefine the enum with the new variant here
# (this simulates what happens in real dev when someone adds to an enum
#  and forgets to update all the switch/match statements)

class DIGIT_V2(Enum):
    ZERO  = 0
    ONE   = 1
    TWO   = 2
    THREE = 3
    FOUR  = 4
    FIVE  = 5   # <-- new variant added, match statements not updated!


def describe_digit_v2(d):
    """original match -- NOT updated for FIVE"""
    match d:
        case DIGIT_V2.ZERO:
            return "zero"
        case DIGIT_V2.ONE:
            return "one"
        case DIGIT_V2.TWO:
            return "two"
        case DIGIT_V2.THREE:
            return "three"
        case DIGIT_V2.FOUR:
            return "four"
        # FIVE is not here -- forgot to add it


def describe_digit_v2_with_default(d):
    """same match but with a wildcard default"""
    match d:
        case DIGIT_V2.ZERO:
            return "zero"
        case DIGIT_V2.ONE:
            return "one"
        case DIGIT_V2.TWO:
            return "two"
        case DIGIT_V2.THREE:
            return "three"
        case DIGIT_V2.FOUR:
            return "four"
        case _:
            return f"[UNHANDLED] {d.name} hit the default!"


# ============================================================
# RUN ALL DEMOS
# ============================================================

print("=" * 55)
print("  PART 1: All Cases Covered")
print("=" * 55)
for d in DIGIT:
    result = describe_digit_full(d)
    print(f"  DIGIT.{d.name:6s} ({d.value}) -> {result}")

print()
print("  Java comparison:")
print("  All cases handled = no warnings, no errors (same behavior)")
print()


print("=" * 55)
print("  PART 2a: Missing Cases, NO Default Wildcard")
print("  (ZERO and THREE deliberately left out)")
print("=" * 55)
for d in DIGIT:
    result = describe_digit_missing(d)
    print(f"  DIGIT.{d.name:6s} ({d.value}) -> {repr(result)}")
print()
print("  Python behavior: returns None silently -- no error, no warning!")
print("  Java (old switch): silently skips -- no output for missing cases")
print("  Java (switch expression, Java 14+): COMPILE ERROR if no default")
print()


print("=" * 55)
print("  PART 2b: Missing Cases, WITH Default Wildcard")
print("  (ZERO and THREE still left out, but _ catches them)")
print("=" * 55)
for d in DIGIT:
    result = describe_digit_missing_with_default(d)
    print(f"  DIGIT.{d.name:6s} ({d.value}) -> {result}")
print()
print("  Python: _ wildcard catches ZERO and THREE silently at runtime")
print("  Java default: same -- catches missing cases but no compile warning")
print()


print("=" * 55)
print("  PART 3a: New Variant (FIVE) Added, Match NOT Updated")
print("  No default wildcard")
print("=" * 55)
for d in DIGIT_V2:
    result = describe_digit_v2(d)
    print(f"  DIGIT_V2.{d.name:6s} ({d.value}) -> {repr(result)}")
print()
print("  Python behavior: FIVE returns None -- silent failure!")
print("  No error, no warning, just None. Very easy to miss in production.")
print()


print("=" * 55)
print("  PART 3b: New Variant (FIVE) Added, Match NOT Updated")
print("  WITH default wildcard")
print("=" * 55)
for d in DIGIT_V2:
    result = describe_digit_v2_with_default(d)
    print(f"  DIGIT_V2.{d.name:6s} ({d.value}) -> {result}")
print()
print("  Python: default catches FIVE and at least you can see it")
print()


# ============================================================
# FINAL ANSWER: What happens when a new variant is added?
# ============================================================
print("=" * 55)
print("  Q: Add a new variant without updating the match --")
print("     warn, compile error, or silent?")
print("=" * 55)
print("""
  PYTHON:
    - No warning. No error. Python runs silently.
    - If there's no wildcard '_', the function returns None.
    - If there IS a wildcard, it falls to the default branch.
    - Python's match/case does NOT enforce exhaustiveness.
    - You'd only catch this with a runtime test or mypy.

  JAVA (old switch statement):
    - Also silent. Missing cases just get skipped.
    - No compile error, no warning by default.

  JAVA (switch expression, Java 14+):
    - COMPILE ERROR if the switch is not exhaustive.
    - Adding FIVE without handling it breaks the build.
    - This is Java's biggest safety advantage over Python.

  VERDICT:
    Java 14+ switch expressions are safer -- the compiler
    forces you to handle every enum case. Python gives you
    nothing. A missing case silently returns None, which can
    cause NullPointerException-style bugs way down the call stack.
""")
