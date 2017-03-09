import re

password = input("Enter a strong password: ")

checkUpper = re.compile(r'\d*\w*[A-Z]\d*\w*')
checkLower = re.compile(r'\d*\w*[a-z]\d*\w*')
checkNumber = re.compile(r'\d*\w*\d+\w*')

cu = checkUpper.search(password)
cl = checkLower.search(password)
cn = checkNumber.search(password)


if cl != None and cu != None and cn != None:
	if cu.group() == cl.group() and cl.group() == cn.group() and len(password) >= 8:
		print("Password %s is strong" % password)
	else:
		print("Password %s is weak" % password)
else:
	print("Password %s is weak" % password)

