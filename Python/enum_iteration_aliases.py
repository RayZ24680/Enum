# enum_iteration_aliases.py
# CS 3350 - Programming Languages
# Topic: Iterating over enums WITHOUT hardcoding, and what happens
#        when two names share the same integer value (aliases).
#
# Questions we're answering:
#   1. Can you iterate all enum values without listing them by hand?
#   2. How much code does it take?
#   3. What if two names get the same integer? Are both shown? Does it error?

from enum import Enum


# =============================================================================
# PART 1: Iterating over all enum values -- no hardcoding required
# =============================================================================
#
# Python's Enum class makes this super easy -- it's completely built in.
# You just throw the enum class into a for-loop and it works.
# No special method calls, no reflection tricks, nothing.
#
# Java equivalent (for comparison):
#   for (Color c : Color.values()) {
#       System.out.println(c);
#   }
# Java also has this built in via .values(), so both languages support it
# natively. Python is arguably cleaner because you don't even need .values().

class Color(Enum):
    RED   = 1
    GREEN = 2
    BLUE  = 3

print("=== PART 1: Basic Iteration (no hardcoding) ===")
print()
print("Just toss the class into a for-loop -- Python handles the rest:")
print()

for color in Color:
    print(f"  name={color.name!r:10s}  value={color.value}")

print()
print("That's it. Built in. 3 lines total (class + for + print).")
print("No reflection, no special imports beyond 'from enum import Enum'.")
print()


# =============================================================================
# PART 2: What about .name, .value, and list() ?
# =============================================================================
#
# You can also dump all members as a list if you need to pass them around
# or count them. Again, zero extra work required.

print("=== PART 2: Other Ways to Get All Members ===")
print()

all_members = list(Color)
print(f"  list(Color)      -> {all_members}")
print(f"  len(Color)       -> {len(Color)}")
print()

# Just the names:
names = [c.name for c in Color]
print(f"  names only       -> {names}")

# Just the values:
values = [c.value for c in Color]
print(f"  values only      -> {values}")
print()


# =============================================================================
# PART 3: Duplicate integer values -- the "alias" problem
# =============================================================================
#
# Here's where things get interesting. What if you assign the SAME integer
# to two different names?
#
# In Python: the second name becomes an ALIAS for the first. It's not a
# separate member -- it just points to the same member. Python does NOT error.
# It silently creates the alias.
#
# Important consequence: when you iterate, aliases are HIDDEN. You only see
# the "canonical" member (the first one defined with that value).
#
# Java comparison:
#   Java *also* allows this without erroring. The second name is just another
#   reference to the same constant. Same behavior -- iterating with .values()
#   in Java also returns only one entry per unique ordinal/value combo.
#
# Side note: if you want Python to FORBID aliases, use enum.unique decorator.
# We'll show that too.

class Status(Enum):
    ACTIVE   = 1
    RUNNING  = 1   # <-- same int as ACTIVE, so this becomes an alias
    STOPPED  = 2
    DEAD     = 2   # <-- same int as STOPPED, alias again
    FINISHED = 3

print("=== PART 3: Duplicate Integer Values (Aliases) ===")
print()
print("Enum definition:")
print("  ACTIVE   = 1")
print("  RUNNING  = 1   # same int -- alias for ACTIVE")
print("  STOPPED  = 2")
print("  DEAD     = 2   # same int -- alias for STOPPED")
print("  FINISHED = 3")
print()

# Show what normal iteration gives us:
print("Normal iteration (for s in Status):  <-- aliases are NOT shown")
for s in Status:
    print(f"  name={s.name!r:12s}  value={s.value}")

print()
print("Notice: RUNNING and DEAD are missing! Python hid them as aliases.")
print(f"Total members seen: {len(list(Status))} (expected 5, got 3)")
print()

# But they still exist -- you can access them directly:
print("But the aliases ARE still accessible directly:")
print(f"  Status.RUNNING          -> {Status.RUNNING}")
print(f"  Status.RUNNING is Status.ACTIVE -> {Status.RUNNING is Status.ACTIVE}")
print(f"  Status.DEAD is Status.STOPPED   -> {Status.DEAD is Status.STOPPED}")
print()
print("So RUNNING isn't a separate object -- it's literally the same object as ACTIVE.")
print()

# Check the aliases dict:
print("Python exposes aliases via _value2member_map_ and __members__:")
print()
print("  Status.__members__  (includes aliases):")
for name, member in Status.__members__.items():
    tag = " <-- ALIAS" if name != member.name else ""
    print(f"    {name!r:12s} -> {member}{tag}")
print()


# =============================================================================
# PART 4: Using enum.unique to FORBID duplicates
# =============================================================================
#
# If you actually want Python to throw an error when you try to use the
# same integer twice, you can slap @enum.unique on top of the class.
# Without this decorator, Python just silently aliases them.

from enum import unique

print("=== PART 4: enum.unique -- Making Duplicates an Error ===")
print()
print("Attempting to create an enum with @unique and duplicate values...")
print()

try:
    @unique
    class StrictStatus(Enum):
        ACTIVE  = 1
        RUNNING = 1   # this will blow up now
        STOPPED = 2

    print("  (no error -- shouldn't reach here)")

except ValueError as e:
    print(f"  ValueError raised: {e}")
    print()
    print("  @unique makes Python enforce that every value is distinct.")
    print("  Without @unique, Python silently aliases. With it, boom.")
print()


# =============================================================================
# PART 5: Summary -- How much code does this take?
# =============================================================================
#
# Iteration with no hardcoding:
#   Python: for x in MyEnum:  -- 1 line, fully built in
#   Java:   for (X x : X.values())  -- 1 line, also built in
#
# Both languages support this natively. Neither needs reflection or hacks.
#
# Duplicate integer behavior:
#   Python: silently creates an alias. Iteration hides duplicates.
#           Use @unique to make it error.
#   Java:   same behavior -- duplicate value creates an alias reference,
#           not a second enum constant. Iterating values() skips aliases.
#
# So the behavior is almost identical between the two languages.

print("=== PART 5: Quick Summary ===")
print()
print("Iteration:")
print("  Python -> 'for x in MyEnum'       -- built in, 1 line")
print("  Java   -> 'for (X x : X.values())'-- built in, 1 line")
print()
print("Duplicate integer (alias) behavior:")
print("  Python -> no error, alias created, hidden during iteration")
print("  Java   -> no error, alias created, hidden during .values()")
print()
print("Preventing duplicates:")
print("  Python -> @enum.unique decorator raises ValueError")
print("  Java   -> no built-in enforcement; would need manual validation")
print()
print("Both names listed when iterating?")
print("  NO -- both languages hide the alias (only canonical name shown).")
print("  The alias IS accessible directly, but iteration skips it.")
