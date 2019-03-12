#!/usr/local/bin/python3
from sys import argv
import string

if __name__ == "__main__":
	file_name = argv[1] 
	fileids = file_name + "-fileids.txt"
	txt = file_name + "-transcription.txt"
	tag_transcription = file_name + "-tag-transcription.txt"
	print(file_name)
	fileid = open(fileids,'r')
	filetxt = open(txt,'r')
	outputFile = open(tag_transcription,'w')
	ids = fileid.readlines()
	lines = filetxt.readlines()
	
	for i in range(len(ids)):
		outputFile.write("<s> {} </s> ({})\n".format(lines[i].strip("\n"),ids[i].strip("\n")))

	fileid.close()
	filetxt.close()
	outputFile.close()