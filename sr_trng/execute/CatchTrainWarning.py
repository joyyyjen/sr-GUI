#!/usr/local/bin/python3
import sys
from sr_trng.definition import PKG_DIR
import os
def catch():
    x = 0
    output_path = os.path.join(PKG_DIR, "output","OOV.txt")
    warning_path = os.path.join(PKG_DIR, "output","training-result.txt")
    pair = {}
    warn = False
    output = open(output_path, 'w')
    with open(warning_path) as f:
        for line in f:
            if "mk_phone_list.c" in line:
                array = line.split()
                word = array[8][1:-1]
                pair[word] = "N"
                x +=1
                warn = True
            if "utt>" in line and warn:
                number = line.split()
                pair[word] = number[1]
                warn = False
    errors = []
    for k in pair:
        errors.append([k,pair[k]])
        output.write("{} {}\n".format(k,pair[k]))
    return errors