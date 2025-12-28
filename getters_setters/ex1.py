class Fruits:
    def __init__(self, name: str):
        self._name = name

    @property
    def fruit_name(self):
        print("returning self._name via fruit_name property method")
        return self._name

    @fruit_name.setter
    def fruit_name(self, value: str):
        print(f"setting self._name to {value} via fruit_name setter method")
        print(f"accessing fruit_name now gives {self.fruit_name}")
        self._name = value

    @fruit_name.deleter
    def fruit_name(self):
        print("self._name was deleted via fruit_name deleter method")
        del self._name


# Example usage:
fruit = Fruits("Banana")


print(fruit.fruit_name)  # Calls the getter
print("=" * 20)


fruit.fruit_name = "Orange"  # Calls the setter
print("=" * 20)


del fruit.fruit_name  # Calls the deleter
print("=" * 20)


# This will raise an AttributeError as _name has been deleted:
try:
    print(fruit.fruit_name)
except AttributeError as e:
    print(
        f"got AttributeError while accessing fruit_name as it has been deleted in last step. e ==> {e}"
    )
print("=" * 20)
