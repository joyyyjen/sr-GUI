''' This program transfer srt file to plain text file that
	punctuation is removed 
	only lower case 
	with each complete sentence in a new line'''

import re
from sys import argv
import string
from nltk.tokenize import wordpunct_tokenize
from num2words import num2words

def detect_num(sentence):
	new_sentence = ''
	tokens = wordpunct_tokenize(sentence)
	ordinal_num = ['st', 'nd', 'rd', 'th']
	for i in tokens:
		if i.isalpha() == False:
			if i[-2:] in ordinal_num:

				new_sentence = new_sentence + num2words(int(i[:-2]),to='ordinal').replace('-',' ') + ' '
				#print('ordinal num\n', new_sentence)
			elif len(i) == 4:
				if '0' == i[1] and i[2] != '0': new_sentence = new_sentence + num2words(int(i)).replace(' and ',' ') + ' '
				else: new_sentence = new_sentence + num2words(int(i), to='year').replace('-',' ') + ' '
			elif 's' in i:

				new_sentence = new_sentence + num2words(int(i[:-1]), to='year').replace('-',' ') + ' '
				#print('year\n', new_sentence)
			elif i.isdigit():
				new_sentence = new_sentence + num2words(int(i)).replace('-',' ') + ' '
			else:
				word = ''
				for char in range(0,len(i)):
					if i[char].isalpha() or i[char] == ':' or i[char] == '[' or i[char] == ']':
						word = word + i[char]
					else: word = word + num2words(int(i[char]))
				new_sentence = new_sentence + word + ' '
				#print('default\n',new_sentence)
		else: new_sentence = new_sentence + i + ' '
	new_sentence = new_sentence.strip(' ')
	return new_sentence

if __name__ == "__main__":
	punct = string.punctuation
	punct = punct.translate({ord(i): None for i in '[]'})
	punct = punct.replace("-", "")
	punct = punct.replace(":", "")
	pattern = str.maketrans('', '', punct)
	#k = 0
	file_name = argv[1] 
	srt = file_name + ".srt"
	txt = file_name + "-transcription.txt"

	file = open(srt,'r')
	outputFile = open(txt,'w')
	lines = file.readlines()
	sentence = ""
	for line in lines:
		# Check if the line has letter
		if re.search('[a-zA-Z]',line) == None: continue
		# Lower Case and Remove punctuation
		line = line.strip('\n').lower()
		
		# Check if the line is complete sentence or not. If is complete, start a new line
		if line[-1] == '.':
			line = line.translate(pattern)
			if '-' in line: line = line.replace('-',' ')
			sentence = sentence + str(line)

			# Save complete sentence to outputFile
			if any(i.isdigit() for i in sentence):
				print(sentence)
				sentence = detect_num(sentence)
				if ': zero oclock' in sentence:
					sentence = sentence.replace(': zero oclock','oclock')
				if ': zero' in sentence:
					sentence = sentence.replace(': zero', 'oclock')
				if 'oclock' in sentence:
					sentence = sentence.replace('oclock','o\'clock')
				print(sentence)
				print()
			outputFile.write('{}\n'.format(sentence))
			sentence = ""
		else:
			line = line.translate(pattern)
			if '-' in line: line = line.replace('-', ' ')
			sentence = sentence + str(line) + ' '
		#k +=1
		#if k ==51: break
	file.close()
	outputFile.close()