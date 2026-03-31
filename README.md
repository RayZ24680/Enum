# Enum — Java vs Python Comparative Study
**CS 3350 — Programming Languages**

A side-by-side exploration of how enumeration types work in Java and Python. Each file targets a specific aspect of enum behavior, with comments throughout that directly compare what each language does, why, and where they differ.

---

## Repository Structure

| File | Language | What It Covers |
|---|---|---|
| `MAIN.java` | Java | Core enum features: declaration, iteration, switch/case, abstract methods, nullability |
| `basic_enum_demo.py` | Python | Direct Python mirror of `MAIN.java` — same enum, same operations |
| `enum_iteration.py` | Python | Simple iteration demo + alias behavior with `__members__` |
| `enum_iteration_aliases.py` | Python | Deep dive: iterating without hardcoding, duplicate integer values (aliases), `@unique` enforcement |
| `enum_match_demo.py` | Python | `match/case` exhaustiveness — full coverage, missing cases, adding new variants |
| `extended_enum_behavior.py` | Python | Associated data, enum methods, ordinal, null/uninitialized enum behavior |

---

## Java — `MAIN.java`

The Java side of the comparison. Compile and run with:

```bash
javac MAIN.java
java MAIN
```

**What it demonstrates:**
- Declaring an enum with a constructor and private field (`DIGIT`)
- Assigning the same integer value to two names (`ONE` and `ONe` both = 1) — Java allows this as long as names differ
- Iterating over all enum values with `DIGIT.values()` and printing their ordinal
- `switch` statement on an enum — missing cases are silently skipped, no compiler error
- Enum with an abstract method overridden per-instance (`SHAPE` with `area()`)
- Uninitialized enum variable — calling a method on it causes a compile warning, not an error

---

## Python — Start Here: `basic_enum_demo.py`

The direct Python equivalent of `MAIN.java`. Run with:

```bash
python basic_enum_demo.py
```

**What it demonstrates:**
- Declaring a `DIGIT` enum using `class DIGIT(Enum)` with explicit integer values
- Accessing `.name`, `.value`, and a custom `.val` attribute
- Iterating with `for digit in DIGIT` (no `.values()` call needed)
- `ValueError` at runtime for out-of-range lookups (vs Java's compile-time prevention)
- Lookup by name: `DIGIT['THREE']` vs Java's `DIGIT.valueOf("THREE")`

---

## Iteration & Aliases — `enum_iteration.py` and `enum_iteration_aliases.py`

```bash
python enum_iteration.py
python enum_iteration_aliases.py
```

**`enum_iteration.py`** — the short version:
- Basic `for` loop over an enum
- What happens when two names share the same integer (`TWO_ALIAS = 2`)
- How `__members__` exposes aliases that iteration hides

**`enum_iteration_aliases.py`** — the full deep dive:
- Iteration without hardcoding any member names (`for x in MyEnum`)
- `list()`, `len()`, name/value list comprehensions
- Duplicate integer behavior: Python silently creates an alias, hides it during iteration, but keeps it accessible
- `Status.RUNNING is Status.ACTIVE` → `True` — they are literally the same object
- `@enum.unique` decorator: makes duplicate values a `ValueError` at class definition time
- Side-by-side behavior summary vs Java

> **Key finding:** Both Java and Python allow duplicate integer values. Neither errors by default. Both hide the alias during iteration. Python has `@unique` to forbid it; Java has no built-in equivalent.

---

## Match / Switch Exhaustiveness — `enum_match_demo.py`

```bash
python enum_match_demo.py
```

**What it demonstrates:**
- `match/case` (Python 3.10+) with all cases covered
- Deliberately missing cases — Python returns `None` silently, no warning
- Adding a new enum variant (`FIVE`) without updating the `match` — Python silently returns `None`
- Wildcard `case _:` as a safety net (equivalent to Java's `default`)

> **Key finding:** Python's `match` is not exhaustiveness-checked. A missing case returns `None` with no error or warning. Java's old `switch` has the same problem, but Java 14+ switch *expressions* require full coverage or a `default` — the first real compile-time safety advantage Java has over Python here.

---

## Associated Data, Methods & Nullability — `extended_enum_behavior.py`

```bash
python extended_enum_behavior.py
```

**What it demonstrates:**

**Shape enum (associated data):**
- Storing a tuple `(label, dimensions_dict)` per member and unpacking it in `__init__`
- Calling `area()` as an enum method dispatching per shape
- Mutating a mutable value inside an enum member — Python allows it, Java's `final` keyword prevents it

**Digit enum (methods + features):**
- `is_even()`, `is_prime()`, `complement()` — methods defined directly on the enum
- Value-based lookup: `Digit(7)` → `SEVEN` (Python has this built in; Java requires a custom static method)
- Name-based lookup: `Digit["THREE"]` vs Java's `Digit.valueOf("THREE")`
- Ordinal workaround: `list(Digit).index(Digit.FIVE)` (Java has `.ordinal()` built in)

**Null / Uninitialized behavior:**
- Setting an enum variable to `None` and calling `.name`, `.area()`, `.dimensions` — all raise `AttributeError`
- Java equivalent: `NullPointerException`
- `None` in a list of enums, `isinstance(None, Shape)` → `False`
- Comparison: `None == Shape.CIRCLE` → `False` (no crash); `None.equals(Shape.CIRCLE)` in Java → NPE

> **Key finding:** Python raises `AttributeError` where Java raises `NullPointerException`. The crash timing is identical (runtime). Java's `@NonNull` annotation and Python's `Optional[MyEnum]` type hint are both opt-in and advisory only.

---

## Requirements

| Language | Requirement |
|---|---|
| Python | Python **3.10+** (for `match/case`). `from enum import Enum` is in the standard library — no pip installs needed. |
| Java | Any modern JDK (Java 8+ for the enum syntax; Java 14+ to see switch expression exhaustiveness behavior) |

---

## Key Takeaways

| Feature | Java | Python |
|---|---|---|
| Iteration | `for (X x : X.values())` | `for x in MyEnum` |
| Duplicate int values | Allowed, silently aliased | Allowed, silently aliased |
| Forbid duplicates | No built-in way | `@enum.unique` |
| Exhaustiveness in switch/match | Enforced in Java 14+ switch *expressions* | Never enforced |
| Value-based lookup | Custom method required | `MyEnum(value)` built in |
| Built-in ordinal | `.ordinal()` | Not built in |
| Null/None behavior | `NullPointerException` | `AttributeError` |
| Associated data | Constructor + private final fields | Tuple + `__init__` |

## AI Usage

Elaborate on differences and similarities between the enums in Java and Python
Gather useful source material from the web
Intellisense Autocomplete code
Work arounds and fixes for exceptions and errors
Provide examples and discription odf real world problems that class type enum was a helpful fix to
