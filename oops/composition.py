class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower
    
    def start(self):
        return "Engine starting with {} horsepower!".format(self.horsepower)

class Car:
    def __init__(self, model, horsepower):
        self.model = model
        # Composition: Car "has-a" Engine as a part of it
        self.engine = Engine(horsepower)
    
    def drive(self):
        return f"{self.model} is driving. {self.engine.start()}"

# Create a Car instance
my_car = Car("Tesla Model 3", 225)
print(my_car.drive())