# The main function that runs all the examples of basic Python operations.
def main():
	# 1) Variables and Data Types
	name = "Alice"           # str
	age = 20                 # int
	height = 1.65            # float
	is_student = True        # bool
	print(name, age, height, is_student)

	# 2) Math Operations
	print("\n")
	a = 10
	b = 3
	print("a + b =", a + b)
	print("a - b =", a - b)
	print("a * b =", a * b)
	print("a / b =", a / b)    # division (float)
	print("a // b =", a // b)  # floor division
	print("a % b =", a % b)    # remainder
	print("a ** b =", a ** b)  # exponent

	# 3) String Operations
	print("\n")
	first = "Hello"
	second = "Python"
	message = first + " " + second
	print(message)
	print("Length:", len(message))
	print("Upper:", message.upper())
	print("Replace:", message.replace("Python", "World"))
	print("Split:", message.split())
	print("Substring:", message[0:5])  # first 5 characters
	print("Last 6 characters:", message[-6:])  # last 6 characters

	# 3.1) f-String Examples
	print("\n")
	city = "Da Nang"
	price = 12.5
	quantity = 4
	total = price * quantity
	print(f"Hello {name}, you are {age} years old.")
	print(f"I live in {city}.")
	print(f"{quantity} items x ${price:.2f} = ${total:.2f}")
	print(f"Next year, age will be {age + 1}.")
	

	# 4) Lists
	print("\n")
	fruits = ["apple", "banana", "orange"]
	print("Original:", fruits)
	fruits.append("mango")
	print("After append:", fruits)
	print("First fruit:", fruits[0])
	print("Last fruit:", fruits[-1])

	# 5) Dictionaries
	print("\n")
	student = {
		"name": "Bob",
		"age": 21,
		"major": "Computer Science",
	}
	print("Student name:", student["name"])
	student["age"] = 22
	student["city"] = "Da Nang"
	print("Updated dictionary:", student)

	# 6) Conditions (if/elif/else)
	print("\n")
	score = 78
	if score >= 90:
		grade = "A"
	elif score >= 75:
		grade = "B"
	else:
		grade = "C"
	print("Score:", score, "-> Grade:", grade)

	# 7) Loops
	print("\n")
	print("For loop:")
	for i in range(1, 6):
		print("i =", i)

	print("While loop:")
	count = 3
	while count > 0:
		print("count =", count)
		count -= 1

	# 8) Functions
	print("\n")

	def add(x, y):
		return x + y

	result = add(5, 7)
	print("add(5, 7) =", result)

	# 9) Decorators
	print("\n")

	def log_function(func):
		"""Decorator that logs function calls"""
		def wrapper(*args, **kwargs):
			print(f"Calling {func.__name__} with args={args}")
			result = func(*args, **kwargs)
			print(f"Result: {result}")
			return result
		return wrapper

	@log_function
	def multiply(x, y):
		return x * y

	multiply(3, 4)  # Will print logs before and after execution

	print("\nDone. Try changing values and run again to learn faster.")


if __name__ == "__main__":
	main()
