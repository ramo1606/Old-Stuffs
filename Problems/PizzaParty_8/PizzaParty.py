while True:
  people = input("How Many People? ")
  pizzas = input("How Many Pizzas do you have? ")
  if people.isnumeric() and pizzas.isnumeric(): 
    break
  else:
    print("Please enter two positive numbers")
    
peopleInt = int(people)
pizzasInt = int(pizzas)

pieces = (pizzasInt * 8) / peopleInt;
leftovers = (pizzasInt * 8) % peopleInt;

print("%i people with %i pizzas" % (peopleInt, pizzasInt))
print("Each person gets %i pieces of pizza.\n" % (pieces))
print("There are %i leftover pieces.\n" % (leftovers))
