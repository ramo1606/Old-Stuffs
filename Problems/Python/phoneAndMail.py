#! python3
# phoneAndEmail.py - Finds phone numbers and email addresses on the clipboard.

import re, pyperclip

phoneRegex = re.compile(r'''(
	(\d{3}|\(\d{3}\))?					#Area Code
	(\s|-|\.)?							#Separator
	(\d{3})								#First 3 Numbers
	(\s|-|\.)							#Separator
	(\d{4})								#Last 4 Numbers
	(\s*(ext|x|ext.)\s*(\d{2,5}))?		#Extension
	)''', re.VERBOSE)
	
mailRegex = re.compile(r'''(
	[a-zA-Z0-9._%+-]+			#Username
	@							#@
	[a-z0-9.-]+					#Domain Name
	(\.[a-zA-Z]{2,4}))			#Dot Something
	)''', re.VERBOSE)
	

text = str(pyperclip.paste())

matches = []

for groups in phoneRegex.find_all(text):
	phoneNumber = '-'.join(groups[1], groups[3], groups[5])
	if(groups[8] != ''):
		phoneNumber += ' X' + groups[8]
	matches.append(phoneNumber)

for groups in mailRegex.find_all(text):
	matches.append(groups[0])
	
if len(matches) > 0:
	pyperclip.copy('\n'.join(matches))
	print('Copied to clipboard: ')
	print('\n'.join(matches))
else:
	print('No phones or emails found in clipboard.')


#TODO Download pyperclip
