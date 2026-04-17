# Mutable vs Immutable and fixing accidental modifications
import copy

# IMMUTABLE: str, int, float, tuple - creates NEW object when modified
print("=== IMMUTABLE OBJECTS ===")
name = "Alice"
print(f"Before: {name} (id: {id(name)})")
name = name + " Nguyen"
print(f"After: {name} (id: {id(name)}) - new object created")

number = 42
old_id = id(number)
number += 1
print(f"\nInt: 42 → {number} (id changed: {old_id != id(number)})")

# MUTABLE: list, dict, set - modifies SAME object
print("\n=== MUTABLE OBJECTS ===")
fruits = ["apple", "banana"]
print(f"Before: {fruits} (id: {id(fruits)})")
fruits.append("orange")
print(f"After: {fruits} (id: {id(fruits)}) - same object modified")

# PROBLEM: Accidental modification
print("\n=== PROBLEM: Accidental Modification ===")
original = [1, 2, 3]
ref = original  # ⚠️ Not a copy!
ref.append(4)
print(f"original: {original}")  # [1, 2, 3, 4] - Accidentally modified!

# FIX 1: Shallow copy (for simple lists)
print("\n=== FIX: SHALLOW COPY ===")
original = [1, 2, 3]
shallow = original.copy()  # or list(original) or original[:]
shallow.append(4)
print(f"original: {original}")  # [1, 2, 3] - Safe!
print(f"shallow: {shallow}")    # [1, 2, 3, 4]

# FIX 2: Deep copy (for nested lists)
print("\n=== FIX: DEEP COPY ===")
original = [["a", "b"], ["c"]]
deep = copy.deepcopy(original)  # Full independent copy
deep[0].append("d")
print(f"original: {original}")  # [['a', 'b'], ['c']] - Safe!
print(f"deep: {deep}")          # [['a', 'b', 'd'], ['c']]

print("\n✓ Use .copy() for simple lists")
print("✓ Use copy.deepcopy() for nested lists")
