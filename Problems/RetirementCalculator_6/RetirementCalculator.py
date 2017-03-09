while True:
  str1 = input("What is your current age? ")
  str2 = input("At what age would you like to retire?: ")
  if str1.isnumeric() and str2.isnumeric(): 
    break
  else:
    print("Please enter two positive numbers")
  
age = int(str1)
year = int(str2)