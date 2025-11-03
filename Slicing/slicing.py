
############################# Some random experiment ###################################
def generate_default_bold():
    print("DEFAULT BOLG GEN called")
    return "="*30

print("before defining separator function")
def separator(msg, bold=generate_default_bold()):
    print(f"{bold} {msg} {bold}")

print("before calling separator")
#######################################################################################





separator("Slicing List") # ==================================================

# Define a list
my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Slice from index 2 to index 6 (remember: stop index is not included)
print(my_list[2:7])    # Output: [2, 3, 4, 5, 6]

# Slice from the beginning to index 3 (i.e., first four elements)
print(my_list[:4])     # Output: [0, 1, 2, 3]

# Slice from index 5 to the end
print(my_list[5:])     # Output: [5, 6, 7, 8, 9]

# Slice with a step of 2 (every second element)
print(my_list[::2])    # Output: [0, 2, 4, 6, 8]

# Slice with a negative step, which reverses the list
print(my_list[::-1])   # Output: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

separator("Slicing String") # ==================================================
# Define a string
my_string = "Hello, world!"

# Slice to get the first five characters
print(my_string[0:5])  # Output: "Hello"

# Slice to get a substring from index 7 to index 11
print(my_string[7:12]) # Output: "world"

# Using a negative step to reverse the string
print(my_string[::-1]) # Output: "!dlrow ,olleH"

separator("Slicing Tuple") # ==================================================

colors = ("red", "green", "blue", "yellow", "purple")

# Get elements from index 1 to 3
subtuple = colors[1:3]
print(subtuple)  # Output: ("green", "blue")

separator("Modifying Sequences") # ==================================================
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Replace a portion of the list
numbers[2:5] = [20, 30, 40]
print(numbers)  # Output: [0, 1, 20, 30, 40, 5, 6, 7, 8, 9]

# Delete a portion of the list
del numbers[3:6]
print(numbers)  # Output: [0, 1, 20, 6, 7, 8, 9]


separator("THE END") # ==================================================