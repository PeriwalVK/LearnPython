class Entity:
    _id_counter = 0

    def __init__(self):
        # Use type(self) to handle inheritance correctly
        type(self)._id_counter += 1
        self.id = type(self)._id_counter

class Person(Entity):
    _id_counter = 0  # Separate counter for Person

class Company(Entity):
    _id_counter = 0  # Separate counter for Company

p1 = Person()
p2 = Person()
c1 = Company()

print(p1.id) # 1
print(p2.id) # 2
print(c1.id) # 1 (Independent of Person's counter)