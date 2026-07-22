import re
from abc import ABC, abstractmethod

class Project(ABC):
    def __init__(self, title):
        self.title = title
       
        self.__client_email = ""

    
    def set_email(self, email):
        self.__client_email = email

    def get_email(self):
        return self.__client_email

    
    @abstractmethod
    def calculate_bill(self):
        pass

    @abstractmethod
    def display(self):
        pass

class FixedProject(Project):
    def __init__(self, title, cost):
        super().__init__(title)
        self.cost = cost

    def calculate_bill(self):
        return self.cost

    def display(self):
        print("\n--- DevTrack: Fixed Project ---")
        print("Project Title:", self.title)
        print("Client Email:", self.get_email())
        print("Billing Type: Flat Rate")
        print("Final Invoice Amount: $", self.calculate_bill())

class HourlyProject(Project):
    def __init__(self, title, hours, rate):
        super().__init__(title)
        self.hours = hours
        self.rate = rate

    def calculate_bill(self):
        return self.hours * self.rate

    def display(self):
        print("\n--- DevTrack: Hourly Project ---")
        print("Project Title:", self.title)
        print("Client Email:", self.get_email())
        print("Billing Type: Hourly Rate")
        print("Total Hours Logged:", self.hours, "hours at $", self.rate, "/hr")
        print("Final Invoice Amount: $", self.calculate_bill())


print("--- Welcome to DevTrack ---")
p_name = input("Enter project name: ")

while True:
    c_email = input("Enter client email: ")
    if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", c_email):
        break
    print("Invalid email format. Please try again.")

choice = input("Enter billing type (fixed / hourly): ").lower().strip()

if choice == "fixed":
    price = float(input("Enter fixed contract price: "))
    project = FixedProject(p_name, price)
else:
    hours_worked = float(input("Enter hours worked: "))
    hourly_rate = float(input("Enter hourly rate: "))
    project = HourlyProject(p_name, hours_worked, hourly_rate)

project.set_email(c_email)
project.display()