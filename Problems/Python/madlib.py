import re

#Open the file and read all the content
fileStr = input("Enter file to read: ")

parseFile = open(fileStr)

fileContent = parseFile.read()

#Setup regex to find all the ADJECTIVE NOUN ADVERB VERB in the text
fileRegex = re.compile(r'ADJECTIVE|NOUN|ADVERB|VERB')

search = fileRegex.findall(fileContent)

#Ask for all the words
replace = []
for word in search:
	if(word == "ADJECTIVE" or word == "ADVERB"):
		replace.append(input("Enter an %s\n" % word.lower()))
	else:
		replace.append(input("Enter a %s\n" % word.lower()))

#Replace all the keywords for the real words
i = 0
for repl in replace:
	fileRegex = re.compile(search[i])
	fileContent = fileRegex.sub(repl, fileContent, 1)
	i = i+1

#Write the new text in a new file
returnFile = open('replaced.txt', 'w')
returnFile.write(fileContent)

#Close the files
parseFile.close()
returnFile.close()
