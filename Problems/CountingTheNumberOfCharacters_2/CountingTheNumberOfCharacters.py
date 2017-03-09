import os

while True:
    mystr = input("Enter a string: ")
    if mystr == "":
        print("Enter a valid string")
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        mystr = mystr + " has " + str(len(mystr)) + " characters."
        break
print(mystr)