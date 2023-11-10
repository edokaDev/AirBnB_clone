#!/usr/bin/python3
from models.base_model import BaseModel

my_model = BaseModel()
my_model.name = "My_First_Model"
my_model.my_number = 89
print("Doing save next")
my_model.save()
print("New object")
print(my_model)
