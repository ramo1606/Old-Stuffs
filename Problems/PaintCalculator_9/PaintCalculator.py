import math

feetPerGallon = 350;
while True:
  length = input("What's the length of the room? ")
  width = input("What's the width of the room? ")
  if length.isnumeric() and width.isnumeric():
    break
  else:
    print("Please enter two positive numbers")

lengthInt = float(length)
widthInt = float(width)

area = lengthInt * widthInt
gallons = math.ceil(area / feetPerGallon)

print("You will need to purchase %f gallons of paint to cover %f square feets" % (gallons, area))
