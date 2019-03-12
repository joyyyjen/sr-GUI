#!/usr/local/bin/python3
''' This program transfer srt file to plain text file that 
	punctuation is removed 
	only lower case 
	with each complete sentence in a new line'''

import re
import os
import string
from nltk.tokenize import wordpunct_tokenize
from num2words import num2words
from sr_trng.definition import PKG_DIR

def find():
    path = os.path.join(PKG_DIR, "model-directory")
    for filename in os.listdir(path):
        if 'srt' in filename:
            return filename
    return []


def detect_num(sentence):
    new_sentence = ''
    tokens = wordpunct_tokenize(sentence)
    ordinal_num = ['st', 'nd', 'rd', 'th']
    for i in tokens:
        if i.isalpha() == False:
            if i[-2:] in ordinal_num:

                new_sentence = new_sentence + num2words(int(i[:-2]), to='ordinal').replace('-', ' ') + ' '
            # print('ordinal num\n', new_sentence)
            elif len(i) == 4:
                if '0' == i[1] and i[2] != '0':
                    new_sentence = new_sentence + num2words(int(i)).replace(' and ', ' ') + ' '
                else:
                    new_sentence = new_sentence + num2words(int(i), to='year').replace('-', ' ') + ' '
            elif 's' in i:

                new_sentence = new_sentence + num2words(int(i[:-1]), to='year').replace('-', ' ') + ' '
            # print('year\n', new_sentence)
            elif i.isdigit():
                new_sentence = new_sentence + num2words(int(i)).replace('-', ' ') + ' '
            else:
                word = ''
                for char in range(0, len(i)):
                    if i[char].isalpha() or i[char] == ':' or i[char] == '[' or i[char] == ']':
                        word = word + i[char]
                    else:
                        word = word + num2words(int(i[char]))
                new_sentence = new_sentence + word + ' '
        # print('default\n',new_sentence)
        else:
            new_sentence = new_sentence + i + ' '
    new_sentence = new_sentence.strip(' ')
    return new_sentence


def script():
    punct = string.punctuation
    punct = punct.translate({ord(i): None for i in '[]'})
    punct = punct.replace("-", "")
    punct = punct.replace(":", "")
    pattern = str.maketrans('', '', punct)

    title = find()
    if title == []: print("error"); return
    txt = os.path.join(PKG_DIR, "model-directory", "trans.txt")
    tag = os.path.join(PKG_DIR, "model-directory", "tag-trans.txt")
    srt_path = os.path.join(PKG_DIR, "model-directory", title)
    fileid_path = os.path.join(PKG_DIR, "model-directory", "fileid.txt")
    fileid = open(fileid_path, 'r')
    ids = fileid.readlines()

    file = open(srt_path, 'r')
    outputFile = open(txt, 'w')
    tag_outputFile = open(tag, 'w')
    lines = file.readlines()
    sentence = ""
    k = 0
    for line in lines:
        # Check if the line has letter
        if re.search('[a-zA-Z]', line) == None: continue
        # Lower Case
        line = line.strip('\n').lower()

        # Check if the line is complete sentence or not. If is complete, start a new line
        if line[-1] == '.':
            # Remove punctuation
            line = line.translate(pattern)
            if '-' in line: line = line.replace('-', ' ')
            sentence = sentence + str(line)

            # Save complete sentence to outputFile
            if any(i.isdigit() for i in sentence):
                #print(sentence)
                sentence = detect_num(sentence)
                if ': zero oclock' in sentence:
                    sentence = sentence.replace(': zero oclock', 'oclock')
                if ': zero' in sentence:
                    sentence = sentence.replace(': zero', 'oclock')
                if 'oclock' in sentence:
                    sentence = sentence.replace('oclock', 'o\'clock')

            if (k > (len(ids)-1)): break
            outputFile.write('{}\n'.format(sentence))
            tag_outputFile.write("<s> {} </s> ({})\n".format(sentence, ids[k].strip("\n")))
            sentence = ""
            k += 1
        else:
            # Remove punctuation
            line = line.translate(pattern)
            if '-' in line: line = line.replace('-', ' ')
            sentence = sentence + str(line) + ' '


    file.close()
    outputFile.close()
    tag_outputFile.close()

#script()