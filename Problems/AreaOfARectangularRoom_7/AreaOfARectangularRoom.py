factor = 0.09290304

while True:
  length = input("What is the length of the room in feet? ")
  width = input("What is the width of the room in feet? ")
  if length.isnumeric() and width.isnumeric(): 
    break
  else:
    print("Please enter two positive numbers")
    
lengthFloat = float(length)
widthFloat = float(width)

feetArea = lengthFloat * widthFloat;
metersArea = feetArea * factor;

print("You entered dimensions of %f feet by %f feet." % (lengthFloat, widthFloat))
print("The area is\n %f square feet\n %f square meters\n" % (feetArea, metersArea))
