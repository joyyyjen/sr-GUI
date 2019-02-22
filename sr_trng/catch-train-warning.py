#!/usr/local/bin/python3
import sys
x = 0
error = open("./Output/catch-error-TedAstrom-result2.txt",'w+')
pair = {}
warn = False
warn2 = False
with open("./TedAstrom_model2/training-result2.txt") as f:
    for line in f:
        if "mk_phone_list.c" in line:
            array = line.split()
            word = array[8]
            pair[word] = "N"
            x +=1
            warn = True
        # Error "utt does not end with filler phone" did produce phonetic transcription
        #elif "cvt2triphone.c" in line:
        #    x+=1
        #    warn2 = True
        #if "utt>" in line and warn2:
        #    number = line.split()
        #    word = "F:" + number[1]
        #    pair[word] = number[1]
        #    warn2 = False

        if "utt>" in line and warn:
            number = line.split()
            pair[word] = number[1]
            warn = False

for k in pair:
    error.write("{} {}\n".format(k,pair[k]))
error.write("{} fail to produce phonetic transcription".format(int(x)/68))