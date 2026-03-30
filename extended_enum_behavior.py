# extended_enum_behavior.py
# CS 3350 - Programming Languages
# Comparing Enums in Python vs Java
# This file shows the Python side of things
# 
# We're looking at how Python enums can carry extra data with each
# variant and what happens when you try to do weird stuff with them
# (like using None as an enum variable, which is kinda like Java's null)

from enum import Enum, unique, auto
import traceback


# ---- PART 1: Basic enum with associated data ----
# In Python you can give each enum member a tuple as its value
# and then unpack it in __init__ to store extra info

class Shape(Enum):
    CIRCLE    = ("circle", {"radius": 5.0})
    RECTANGLE = ("rectangle", {"width": 4.0, "height": 7.0})
    TRIANGLE  = ("triangle", {"base": 3.0, "height": 5.0})
    POINT     = ("point", {})  # this one has no real data

    def __init__(self, label, dimensions):
        self.label = label
        self.dimensions = dimensions

    def area(self):
        """calculate the area based on what shape it is"""
        import math
        if self.label == "circle":
            return math.pi * self.dimensions["radius"] ** 2
        elif self.label == "rectangle":
            return self.dimensions["width"] * self.dimensions["height"]
        elif self.label == "triangle":
            return 0.5 * self.dimensions["base"] * self.dimensions["height"]
        else:
            return 0.0


# ---- PART 2: Enum that also acts like a string ----
# This is useful for stuff like HTTP status codes where you want
# the enum to literally be usable as a string

class HttpStatus(str, Enum):
    OK             = "OK"
    NOT_FOUND      = "Not Found"
    INTERNAL_ERROR = "Internal Server Error"
    TEAPOT         = "I'm a teapot"

    def __new__(cls, phrase):
        obj = str.__new__(cls, phrase)
        obj._value_ = phrase
        return obj

    def __init__(self, phrase):
        codes = {
            "OK": (200, "success"),
            "Not Found": (404, "client_error"),
            "Internal Server Error": (500, "server_error"),
            "I'm a teapot": (418, "easter_egg"),
        }
        self.code, self.severity = codes[phrase]

    def is_error(self):
        return self.code >= 400


# ---- PART 3: Tagged union pattern ----
# Python enums can't do what Rust does natively where each variant
# has different fields, but we can fake it with a wrapper class

class Result(Enum):
    SUCCESS = auto()
    ERROR   = auto()
    PENDING = auto()

class ResultValue:
    """pairs a Result tag with whatever data you want"""
    def __init__(self, tag, **payload):
        self.tag = tag
        self.payload = payload

    def __repr__(self):
        items = ", ".join(f"{k}={v!r}" for k, v in self.payload.items())
        return f"ResultValue({self.tag.name}, {items})"

    def unwrap(self):
        if self.tag is Result.ERROR:
            raise RuntimeError(f"tried to unwrap an error: {self.payload.get('message', '?')}")
        return self.payload


# ---- PART 4: Log levels with per-member behavior ----
# You can actually override methods on individual enum members
# which is kinda cool

class LogLevel(Enum):
    DEBUG   = 10
    INFO    = 20
    WARNING = 30
    ERROR   = 40

    def format_message(self, msg):
        return f"[{self.name}] {msg}"


# monkey-patch specific members to have different formatting
import types
LogLevel.ERROR.format_message = types.MethodType(
    lambda self, msg: f"[!] ERROR: {msg.upper()}", LogLevel.ERROR
)
LogLevel.WARNING.format_message = types.MethodType(
    lambda self, msg: f"[*] WARN: {msg}", LogLevel.WARNING
)


# ========================================
#   HELPER - just prints section headers
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
    print_section("1. Shape Enum - Tuple-Based Data")

    for s in Shape:
        print(f"  {s.name:12s}  label={s.label!r:14s}  "
              f"dims={s.dimensions}  area={s.area():.4f}")

    print(f"\n  CIRCLE radius: {Shape.CIRCLE.dimensions['radius']}")

    # you can look up a shape by its full tuple value
    found = Shape(("circle", {"radius": 5.0}))
    print(f"  Lookup by value: {found} is CIRCLE? {found is Shape.CIRCLE}")

    # --- 2. HTTP status demo ---
    print_section("2. HttpStatus Enum - String Mixin")

    for status in HttpStatus:
        print(f"  {status.name:20s}  code={status.code}  "
              f"severity={status.severity:14s}  is_error={status.is_error()}")

    # since it inherits from str, you can do string ops
    print(f"\n  Upper-cased: {HttpStatus.TEAPOT.upper()}")
    print(f"  Concatenation: {'Status: ' + HttpStatus.OK}")

    # --- 3. Tagged union demo ---
    print_section("3. Result + ResultValue - Tagged Union")

    ok   = ResultValue(Result.SUCCESS, data=[1, 2, 3])
    err  = ResultValue(Result.ERROR, message="disk full", code=28)
    pend = ResultValue(Result.PENDING, eta_seconds=45)

    for rv in (ok, err, pend):
        print(f"  {rv}")

    print(f"\n  Unwrap SUCCESS: {ok.unwrap()}")

    # --- 4. LogLevel per-member overrides ---
    print_section("4. LogLevel - Per-Member Method Overrides")

    msg = "something went wrong"
    for level in LogLevel:
        print(f"  {level.format_message(msg)}")

    # ============================================================
    #   EDGE CASES AND WEIRD STUFF
    # ============================================================
    print_section("5. Edge Cases & Unexpected Usage")

    # 5a. accessing a key that doesn't exist
    print("\n  5a. Accessing missing dimension on POINT:")
    try:
        _ = Shape.POINT.dimensions["radius"]
    except KeyError as e:
        print(f"      KeyError: {e}  (POINT doesn't have 'radius')")

    # 5b. looking up a shape that doesn't exist
    print("\n  5b. Looking up a non-existent Shape:")
    try:
        _ = Shape(("hexagon", {"sides": 6}))
    except ValueError as e:
        print(f"      ValueError: {e}")

    # 5c. trying to add a new enum member at runtime
    print("\n  5c. Adding a member at runtime:")
    try:
        Shape.PENTAGON = ("pentagon", {"sides": 5})
        is_real = isinstance(Shape.PENTAGON, Shape)
        print(f"      No exception but is it a real member? {is_real}")
        if not is_real:
            print("      Nope - it's just a plain attribute, not an enum member")
        try:
            del Shape.PENTAGON
        except AttributeError:
            pass
    except AttributeError as e:
        print(f"      AttributeError: {e}")

    # 5d. trying to reassign an existing member
    print("\n  5d. Reassigning Shape.CIRCLE:")
    try:
        Shape.CIRCLE = ("ellipse", {"a": 3, "b": 5})
    except AttributeError as e:
        print(f"      AttributeError: {e}")

    # 5e. mutating mutable data inside an enum member
    # THIS ACTUALLY WORKS which is kind of scary
    print("\n  5e. Mutating the dict inside Shape.CIRCLE:")
    old_radius = Shape.CIRCLE.dimensions["radius"]
    Shape.CIRCLE.dimensions["radius"] = 999
    print(f"      radius was {old_radius}, now {Shape.CIRCLE.dimensions['radius']}")
    print("      Python lets you mutate mutable data inside enums!")
    Shape.CIRCLE.dimensions["radius"] = old_radius  # put it back

    # 5f. unwrapping an error result
    print("\n  5f. Unwrapping an ERROR result:")
    try:
        err.unwrap()
    except RuntimeError as e:
        print(f"      RuntimeError: {e}")

    # 5g. duplicate values with @unique
    print("\n  5g. Duplicate values with @unique:")
    try:
        @unique
        class Color(Enum):
            RED  = 1
            RUBY = 1  # same value as RED
    except ValueError as e:
        print(f"      ValueError: {e}")

    # 5h. comparing enums from different classes
    print("\n  5h. Cross-enum comparison:")
    result = Shape.CIRCLE == HttpStatus.OK
    print(f"      Shape.CIRCLE == HttpStatus.OK -> {result}  (always False)")

    # 5i. enum members as dict keys
    print("\n  5i. Enum members as dictionary keys:")
    costs = {Shape.CIRCLE: 9.99, Shape.RECTANGLE: 14.50}
    print(f"      costs[Shape.CIRCLE] = {costs[Shape.CIRCLE]}")

    # 5j. identity vs equality
    print("\n  5j. Identity (is) vs equality (==):")
    a = Shape.CIRCLE
    b = Shape(("circle", {"radius": 5.0}))
    print(f"      a == b: {a == b}")
    print(f"      a is b: {a is b}  (singletons!)")

    # ============================================================
    #   *** NULL / UNINITIALIZED ENUM VARIABLE ***
    #   This is the big one for our Java vs Python comparison.
    #   In Java, an uninitialized enum variable is null and calling
    #   a method on it throws NullPointerException.
    #   In Python, the closest equivalent is setting a variable to
    #   None and then trying to use it like an enum.
    # ============================================================
    print_section("6. Null / Uninitialized Enum Variable")

    # 6a. set an enum variable to None (Python's version of null)
    print("\n  6a. Setting an enum variable to None and calling .name:")
    my_shape = None  # like an uninitialized enum in Java
    try:
        print(f"      my_shape.name = {my_shape.name}")
    except AttributeError as e:
        print(f"      AttributeError: {e}")
        print("      In Java this would be a NullPointerException!")

    # 6b. try to call a method on the None variable
    print("\n  6b. Calling .area() on a None variable:")
    try:
        print(f"      my_shape.area() = {my_shape.area()}")
    except AttributeError as e:
        print(f"      AttributeError: {e}")
        print("      Same thing - Python says 'NoneType' has no attribute 'area'")

    # 6c. try to access associated data on None
    print("\n  6c. Accessing .dimensions on a None variable:")
    try:
        print(f"      my_shape.dimensions = {my_shape.dimensions}")
    except AttributeError as e:
        print(f"      AttributeError: {e}")

    # 6d. try to use None in a match/if statement meant for enums
    print("\n  6d. Using None in comparisons meant for enums:")
    my_status = None
    if my_status == HttpStatus.OK:
        print("      Status is OK")
    elif my_status is None:
        print("      Status is None! No crash, but no useful data either")
        print("      Java would crash here if you called .code on null")

    # 6e. passing None to a function that expects an enum
    print("\n  6e. Passing None where an enum is expected:")
    def get_status_code(status):
        """this function assumes it gets an HttpStatus"""
        return status.code  # will blow up if status is None
    try:
        code = get_status_code(None)
    except AttributeError as e:
        print(f"      AttributeError: {e}")
        print("      Python doesn't have type enforcement at runtime for this")

    # 6f. putting None into a list of enum values and iterating
    print("\n  6f. None mixed into a list of enum values:")
    shapes_list = [Shape.CIRCLE, None, Shape.TRIANGLE]
    for i, s in enumerate(shapes_list):
        try:
            print(f"      shapes_list[{i}]: area = {s.area():.4f}")
        except AttributeError:
            print(f"      shapes_list[{i}]: AttributeError - it's None!")

    # 6g. type checking None against the enum type
    print("\n  6g. isinstance check with None:")
    print(f"      isinstance(Shape.CIRCLE, Shape) = {isinstance(Shape.CIRCLE, Shape)}")
    print(f"      isinstance(None, Shape)         = {isinstance(None, Shape)}")
    print("      Unlike Java, Python's isinstance gives False instead of crashing")

    # 6h. storing None as a default and forgetting to initialize
    print("\n  6h. Simulating 'forgot to initialize' pattern:")

    class Config:
        """imagine this is some config class where you forgot to set the log level"""
        def __init__(self):
            self.log_level = None  # oops, forgot to set this to a real LogLevel

    config = Config()
    try:
        formatted = config.log_level.format_message("hello")
    except AttributeError as e:
        print(f"      AttributeError: {e}")
        print("      This is exactly what happens in Java with null enums!")
        print("      Java: NullPointerException")
        print("      Python: AttributeError on NoneType")

    # --- summary ---
    print_section("Summary")
    print("""
  KEY FINDINGS FOR JAVA VS PYTHON ENUM COMPARISON:

  1. Python doesn't really have "null" enums the way Java does.
     You can set a variable to None, but Python won't stop you.
     Java at least has the type system to warn you (with Optional, etc.)

  2. When you DO access stuff on None in Python you get AttributeError,
     which is basically Python's equivalent of Java's NullPointerException.

  3. Python enums can carry associated data through tuples and __init__,
     while Java enums have actual fields and constructors (more structured).

  4. Python allows mutable data inside enum members (kinda dangerous).
     Java enum fields can be final, preventing this.

  5. Both languages prevent adding new enum members at runtime.

  6. Neither language has great built-in exhaustiveness checking for
     enum switches/matches (though Java 17+ sealed classes help).
""")


if __name__ == "__main__":
    main()
