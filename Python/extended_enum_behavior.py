# extended_enum_behavior.py
# CS 3350 - Programming Languages
# Comparing Enums in Python vs Java
# 
# This file demonstrates three enum patterns:
#   1. Shape enum - carrying associated data (tuples)
#   2. Digit enum - simple value mapping with methods
#   3. Null/uninitialized enum variable behavior

from enum import Enum, unique
import traceback


# ---- PART 1: Shape enum with associated data ----
# Each enum member stores a tuple that gets unpacked into attributes.
#
# JAVA COMPARISON:
#   In Java, you'd write this with a constructor and final fields:
#
#   public enum Shape {
#       CIRCLE("circle", Map.of("radius", 5.0)),
#       RECTANGLE("rectangle", Map.of("width", 4.0, "height", 7.0)),
#       TRIANGLE("triangle", Map.of("base", 3.0, "height", 5.0)),
#       POINT("point", Map.of());
#
#       private final String label;
#       private final Map<String, Double> dimensions;
#
#       Shape(String label, Map<String, Double> dimensions) {
#           this.label = label;
#           this.dimensions = dimensions;
#       }
#   }
#
# Key difference: Java fields are typically 'final', so you CAN'T
# accidentally mutate them. Python has no such protection.

class Shape(Enum):
    CIRCLE    = ("circle",    {"radius": 5.0})
    RECTANGLE = ("rectangle", {"width": 4.0, "height": 7.0})
    TRIANGLE  = ("triangle",  {"base": 3.0, "height": 5.0})
    POINT     = ("point",     {})  # no dimensions

    def __init__(self, label, dimensions):
        self.label = label
        self.dimensions = dimensions

    def area(self):
        """calculate area based on the shape type"""
        import math
        if self.label == "circle":
            return math.pi * self.dimensions["radius"] ** 2
        elif self.label == "rectangle":
            return self.dimensions["width"] * self.dimensions["height"]
        elif self.label == "triangle":
            return 0.5 * self.dimensions["base"] * self.dimensions["height"]
        else:
            return 0.0


# ---- PART 2: Digit enum ----
# Maps digit names to their integer values, with helper methods.
#
# JAVA COMPARISON:
#   public enum Digit {
#       ZERO(0), ONE(1), TWO(2), THREE(3), FOUR(4),
#       FIVE(5), SIX(6), SEVEN(7), EIGHT(8), NINE(9);
#
#       private final int value;
#
#       Digit(int value) { this.value = value; }
#       public int getValue() { return value; }
#       public boolean isEven() { return value % 2 == 0; }
#       public Digit complement() { return values()[9 - value]; }
#   }
#
# Differences:
#   - Java: the value is stored in a private final field, accessed via getter
#   - Python: the value IS the enum's .value attribute directly
#   - Java: complement() uses values()[index] to look up by ordinal
#   - Python: we have to filter through the enum members manually
#   - Java: enums have a built-in .ordinal() method
#   - Python: no ordinal, but you can use list(Digit).index(member)

@unique
class Digit(Enum):
    ZERO  = 0
    ONE   = 1
    TWO   = 2
    THREE = 3
    FOUR  = 4
    FIVE  = 5
    SIX   = 6
    SEVEN = 7
    EIGHT = 8
    NINE  = 9

    def is_even(self):
        """check if this digit is even"""
        return self.value % 2 == 0

    def complement(self):
        """return the 9's complement (9 - digit)"""
        complement_val = 9 - self.value
        return Digit(complement_val)

    def to_word(self):
        """return the English word for this digit"""
        # in Java you'd probably store this as another field in the constructor
        # like Digit(0, "zero") with a 'word' field
        # Python lets us just use .name.lower() since the names ARE the words
        return self.name.lower()

    def is_prime(self):
        """check if this digit is a prime number"""
        return self.value in {2, 3, 5, 7}


# ========================================
#   HELPER
# ========================================
def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ========================================
#   MAIN DEMO
# ========================================
def main():

    # --- 1. Shape enum demo ---
    print_section("1. Shape Enum - Associated Data")

    for s in Shape:
        print(f"  {s.name:12s}  label={s.label!r:14s}  "
              f"dims={s.dimensions}  area={s.area():.4f}")

    print(f"\n  CIRCLE radius: {Shape.CIRCLE.dimensions['radius']}")

    # lookup by full tuple value
    found = Shape(("circle", {"radius": 5.0}))
    print(f"  Lookup by value: {found} is CIRCLE? {found is Shape.CIRCLE}")

    # --- Shape edge cases ---
    print_section("1b. Shape Edge Cases")

    # accessing a key that doesn't exist
    print("\n  Accessing missing dimension on POINT:")
    try:
        _ = Shape.POINT.dimensions["radius"]
    except KeyError as e:
        print(f"      KeyError: {e}  (POINT has no 'radius')")
        # Java equivalent: map.get("radius") returns null,
        # and unboxing null to double throws NullPointerException

    # mutating mutable data inside an enum (this is dangerous!)
    print("\n  Mutating the dict inside Shape.CIRCLE:")
    old_radius = Shape.CIRCLE.dimensions["radius"]
    Shape.CIRCLE.dimensions["radius"] = 999
    print(f"      radius was {old_radius}, now {Shape.CIRCLE.dimensions['radius']}")
    print("      Python lets you mutate mutable data inside enums!")
    print("      In Java, if the field is 'final', this would be a compile error.")
    Shape.CIRCLE.dimensions["radius"] = old_radius  # put it back

    # trying to reassign an enum member
    print("\n  Trying to reassign Shape.CIRCLE:")
    try:
        Shape.CIRCLE = ("ellipse", {"a": 3, "b": 5})
    except AttributeError as e:
        print(f"      AttributeError: {e}")
        print("      Same in Java - enum constants can't be reassigned")

    # --- 2. Digit enum demo ---
    print_section("2. Digit Enum")

    print("  All digits:")
    for d in Digit:
        comp = d.complement()
        print(f"    {d.to_word():>5s} ({d.value})  "
              f"even={str(d.is_even()):>5s}  "
              f"prime={str(d.is_prime()):>5s}  "
              f"9s complement={comp.to_word()} ({comp.value})")

    # --- Digit-specific features ---
    print_section("2b. Digit Features & Java Comparison")

    # lookup by value (Python) vs valueOf by name (Java)
    print("\n  Lookup by integer value:")
    d = Digit(7)
    print(f"      Digit(7) = {d.name}")
    print("      Java equivalent: no direct equivalent!")
    print("      Java's valueOf() only works with strings: Digit.valueOf(\"SEVEN\")")
    print("      To lookup by int in Java you'd need a custom static method")

    # lookup by name
    print("\n  Lookup by name:")
    d2 = Digit["THREE"]
    print(f"      Digit['THREE'] = {d2.name} (value={d2.value})")
    print("      Java equivalent: Digit.valueOf(\"THREE\")")

    # iteration comparison
    print("\n  Iteration:")
    names = [d.name for d in Digit]
    print(f"      Python: for d in Digit -> {names[:4]}...")
    print("      Java:   for (Digit d : Digit.values()) -> same thing")
    print("      Python iteration is simpler syntax-wise")

    # ordinal comparison
    print("\n  Ordinal / Index:")
    idx = list(Digit).index(Digit.FIVE)
    print(f"      Python: list(Digit).index(Digit.FIVE) = {idx}")
    print("      Java:   Digit.FIVE.ordinal() = 5")
    print("      Java has built-in ordinal(), Python needs a workaround")

    # identity check
    print("\n  Identity (singleton check):")
    a = Digit(3)
    b = Digit.THREE
    print(f"      Digit(3) is Digit.THREE -> {a is b}")
    print("      Both Python and Java enums are singletons")
    print("      Java: Digit.THREE == Digit.valueOf(\"THREE\") -> true (same object)")

    # using enums in arithmetic (Python allows it, Java doesn't directly)
    print("\n  Using enum .value in arithmetic:")
    result = Digit.THREE.value + Digit.FOUR.value
    print(f"      Digit.THREE.value + Digit.FOUR.value = {result}")
    print("      Python: works directly with .value")
    print("      Java: Digit.THREE.getValue() + Digit.FOUR.getValue()")
    print("      Both need explicit access to the underlying int")

    # ============================================================
    #   *** NULL / UNINITIALIZED ENUM VARIABLE ***
    #   In Java, an uninitialized enum variable is null.
    #   Calling any method on it throws NullPointerException.
    #   In Python, the closest thing is setting a variable to None.
    # ============================================================
    print_section("3. Null / Uninitialized Enum Variable")

    # 3a. None as a Shape
    print("\n  3a. Setting a Shape variable to None and calling .name:")
    my_shape = None  # like Shape myShape = null; in Java
    try:
        print(f"      my_shape.name = {my_shape.name}")
    except AttributeError as e:
        print(f"      AttributeError: {e}")
        print("      Java: NullPointerException: Cannot invoke \"Shape.name()\"")

    # 3b. calling a method on None
    print("\n  3b. Calling .area() on a None variable:")
    try:
        print(f"      my_shape.area() = {my_shape.area()}")
    except AttributeError as e:
        print(f"      AttributeError: {e}")
        print("      Java: NullPointerException")

    # 3c. accessing associated data on None
    print("\n  3c. Accessing .dimensions on None:")
    try:
        print(f"      my_shape.dimensions = {my_shape.dimensions}")
    except AttributeError as e:
        print(f"      AttributeError: {e}")

    # 3d. None Digit - trying to call methods
    print("\n  3d. Setting a Digit variable to None and calling .is_even():")
    my_digit = None  # like Digit myDigit = null; in Java
    try:
        print(f"      my_digit.is_even() = {my_digit.is_even()}")
    except AttributeError as e:
        print(f"      AttributeError: {e}")
        print("      Java: NullPointerException")

    # 3e. trying complement on None
    print("\n  3e. Calling .complement() on a None Digit:")
    try:
        print(f"      my_digit.complement() = {my_digit.complement()}")
    except AttributeError as e:
        print(f"      AttributeError: {e}")

    # 3f. None in comparisons
    print("\n  3f. Comparing None to an actual enum value:")
    my_shape = None
    if my_shape == Shape.CIRCLE:
        print("      It's a circle")
    elif my_shape is None:
        print("      my_shape is None - no crash on comparison!")
        print("      Java: myShape == Shape.CIRCLE works too (no NPE)")
        print("      But myShape.equals(Shape.CIRCLE) WOULD throw NPE!")

    # 3g. isinstance check
    print("\n  3g. isinstance check with None:")
    print(f"      isinstance(Shape.CIRCLE, Shape)  = {isinstance(Shape.CIRCLE, Shape)}")
    print(f"      isinstance(None, Shape)           = {isinstance(None, Shape)}")
    print(f"      isinstance(Digit.FIVE, Digit)     = {isinstance(Digit.FIVE, Digit)}")
    print(f"      isinstance(None, Digit)            = {isinstance(None, Digit)}")
    print("      Java: (null instanceof Shape) -> false (no crash)")

    # 3h. passing None to a function expecting an enum
    print("\n  3h. Passing None to a function that expects an enum:")
    def describe_shape(s):
        return f"{s.label} with area {s.area():.2f}"
    try:
        print(f"      {describe_shape(None)}")
    except AttributeError as e:
        print(f"      AttributeError: {e}")
        print("      Python has no compile-time check for this!")
        print("      Java would catch Shape s = null at compile time")
        print("      if you used @NonNull annotation")

    # 3i. None in a list of enums
    print("\n  3i. None mixed into a list of enum values:")
    digits_list = [Digit.ONE, None, Digit.THREE]
    for i, d in enumerate(digits_list):
        try:
            print(f"      digits_list[{i}]: {d.to_word()} is_prime={d.is_prime()}")
        except AttributeError:
            print(f"      digits_list[{i}]: AttributeError - it's None!")

    # 3j. the "forgot to initialize" pattern
    print("\n  3j. Simulating 'forgot to initialize' pattern:")

    class Calculator:
        def __init__(self):
            self.base = None  # oops, should be a Digit

    calc = Calculator()
    try:
        result = calc.base.complement()
    except AttributeError as e:
        print(f"      AttributeError: {e}")
        print("      This is the classic uninitialized-enum bug!")
        print("      Java:  NullPointerException")
        print("      Python: AttributeError on NoneType")

    # --- summary ---
    print_section("Summary")
    print("""
  PYTHON vs JAVA ENUM COMPARISON:

  Shape Enum (associated data):
    - Python: tuple values + __init__ unpacking
    - Java:   constructor params + final fields
    - Java is safer (final prevents mutation)
    - Python is more flexible (any data type, mutable)

  Digit Enum (simple values with methods):
    - Python: value IS the int, methods access self.value
    - Java:   int stored in private field, accessed via getter
    - Python has value-based lookup: Digit(7)
    - Java only has name-based lookup: Digit.valueOf("SEVEN")
    - Java has built-in .ordinal(), Python doesn't

  Null / Uninitialized Enums:
    - Python None -> AttributeError on any attribute access
    - Java null  -> NullPointerException on any method call
    - Both crash at RUNTIME, not compile time
    - Java can use @NonNull annotations for compile-time warnings
    - Python can use mypy type hints for static analysis
    - Neither language fully prevents the null-enum problem
""")


if __name__ == "__main__":
    main()
