taxRate = 0.055;
addItem = "yes"
moreItems = True
itemCount = 1
itemList = {}
while moreItems:
	item = input("Enter the price of item %i: " % itemCount)
	quantity = input("Enter the quantity of item %i: " % itemCount)
	if item.isnumeric() and quantity.isnumeric():
		itemList[item] = quantity
		addItem = input("Add another item? ")
		while True:
			if addItem.lower() == "yes" or addItem.lower() == "y":
				itemCount += 1
				break
			if addItem.lower() == "no" or addItem.lower() == "n":
				moreItems = False
				break
			else:
				print("Please enter yes or no")
				continue
	else:
		print("Please enter two positive numbers")

subtotal = 0

for item, quantity in itemList.items():
	subtotal += float(item) * int(quantity)
	
tax = subtotal * taxRate
total = subtotal + tax

print("Subtotal: %f" % (subtotal))
print("Taxes: %f" % (tax))
print("Total: %f" % (total))


#TO DO: Check if isnumeric() works for floats
