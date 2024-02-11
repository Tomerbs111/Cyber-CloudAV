class Name:
    def __init__(self, value):
        self.value = value

# Your string representation of the class
x = "Name"

# Retrieve the class from the global namespace using globals()
class_instance = globals()[x]("John Doe")

# Now class_instance is an instance of the Name class
print(class_instance.value)  # Output: John Doe


