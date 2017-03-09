usRate = 1.14;
rateDictionary = {}
#while True:
currency = input("What currency do you want to exchange?: ")
amount = input("How Many %s are you exchanging?: " % currency)
rate = input("What is the exchange rate? ")
	#if amount.isnumeric() and rate.isnumeric():
	#	rateDictionary[currency] = rate
	#	break
	#else:
	#	print("Please enter two positive numbers")

amountFloat = float(amount)
rateFloat = float(rate)
total = (amountFloat*rateFloat)/usRate

print("%f %s at an exchange rate of %f is %f U.S. Dollars" % (amountFloat, currency, rateFloat, total))


#TO DO: Check if isnumeric() works for floats
