while True:
  str1 = input("Enter first number: ")
  str2 = input("Enter second number: ")
  if str1.isnumeric() and str2.isnumeric(): 
    break
  else:
    print("Please enter two positive numbers")
  
num1 = int(str1)
num2 = int(str2)

add = num1 + num2
dif = num1 - num2
prod = num1 * num2
quot = num1 / num2

print("%i + %i = %i\n" % (num1, num2, add) + "%i - %i = %i\n" % (num1, num2, dif) + "%i * %i = %i\n" % (num1, num2, prod) + "%i / %i = %i\n" % (num1, num2, quot))
