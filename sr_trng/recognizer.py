#!/usr/local/bin/python3

import os
from pocketsphinx import AudioFile, get_model_path, get_data_path
import speech_recognition as sr

model_path = get_model_path()
cwd = os.getcwd()

#=== TRAIN MODELS===#

hmm_train1= cwd + '/Ted_model1/model1'
hmm_train2= cwd + '/TedAstrom_model2/model2'
hmm_train4= cwd + '/TedAstrom_model2/model2-update-dict'
#lm_train = cwd+'/model3.lm.bin'
dict_train = cwd+'/TrainingSet/cmudict-en-us.dict'

#=== DEFAULT ===#
hmm= model_path+'/en-us'
lm = model_path+'/en-us.lm.bin'
#dict1 = model_path +'/cmudict-en-us.dict'
#print(dict1)


r = sr.Recognizer()
'''
file1 = open("./Output/CMU-D-Ted-recognition.txt",'w+')
file2 = open( "./Output/CMU-T-Ted-recognition.txt", 'w+')
with open('./TedAstrom_model2/ted.fileids','r') as f:
	for id in f:
		path = "./TedAstrom_model2/"+id.strip('\n')+".wav"
		AudioCollection = sr.AudioFile(path)
		with AudioCollection as source:
			audio = r.record(source)
			#====CMUSphinx1====#
			print(r.recognize_sphinx(audio_data = audio,language = (hmm_train1,lm,dict1)))
			file1.write('{}\n'.format(r.recognize_sphinx(audio_data = audio,language = (hmm,lm,dict1))))
			file2.write('{}\n'.format(r.recognize_sphinx(audio_data = audio,language = (hmm_train1,lm,dict1))))
'''
print("******** Session Model3 **********")
#file3 = open("./Output/CMU-D2-Astrom-recognition.txt",'w+')
file4 = open("./Output/CMU-T5-Astrom-recognition.txt",'w+')
with open('./TedAstrom_model2/Astrom.fileids') as f:
	for id in f:
		path = "./TedAstrom_model2/"+id.strip('\n')+".wav"
		AudioCollection = sr.AudioFile(path)
		with AudioCollection as source:
			audio = r.record(source)
			#====CMUSphinx1====#
			#print(r.recognize_sphinx(audio_data = audio,language = (hmm_train,lm,dict1)))
			#file3.write('{}\n'.format(r.recognize_sphinx(audio_data = audio,language = (hmm,lm,dict1))))
			file4.write('{}\n'.format(r.recognize_sphinx(audio_data = audio,language = (hmm_train4,lm,dict_train))))
print("******** Session2-2 **********")
file5 = open("./Output/CMU-T5-Ted-recognition.txt",'w+')
with open('./TedAstrom_model2/ted.fileids') as f:
	for id in f:
		path = "./TedAstrom_model2/"+id.strip('\n')+".wav"
		AudioCollection = sr.AudioFile(path)
		with AudioCollection as source:
			audio = r.record(source)
			#====CMUSphinx1====#
			#print(r.recognize_sphinx(audio_data = audio,language = (hmm_train,lm,dict1)))
			#print(r.recognize_sphinx(audio_data = audio,language = (hmm,lm,dict1)))
			file5.write('{}\n'.format(r.recognize_sphinx(audio_data = audio,language = (hmm_train4,lm,dict_train))))


#file1.close()
#file2.close()
#file3.close()
file4.close()
file5.close()


