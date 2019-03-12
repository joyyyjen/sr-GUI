#!/usr/local/bin/python3

import os
from pocketsphinx import AudioFile, get_model_path, get_data_path
import speech_recognition as sr
import progressbar
from time import sleep

model_path = get_model_path()
cwd = os.getcwd()

#=== TRAIN ===#

#hmm_train= cwd + '/acoustic-model'
#lm_train = cwd+'/model3.lm.bin'
#dict1_train = cwd+'/models/lexiconc.dict'

#=== DEFAULT ===#
hmm= model_path+'/en-us'
lm = model_path+'/en-us.lm.bin'
dict1 = model_path +'/cmudict-en-us.dict'
#print(hmm_train,lm,dict1)

bar = progressbar.ProgressBar(maxval=462, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

r = sr.Recognizer()
#file1=  open("/Ouput/CMUoutputTed1.txt",'w+')
#file2 = open("Output/GoogleouputTed1.txt",'w+')
bar.start()
x = 0
with open('/Users/joyjen/Projects/ErrorClasses/audio-trans-id/audio-fileids-2.txt','r') as f: 
	for id in f:
		path = "/Users/joyjen/Projects/ErrorClasses/refined-audio/"+id.strip('\n')+".wav"
		#print(path)
		AudioCollection = sr.AudioFile(path)
		with AudioCollection as source:
			audio = r.record(source)
			#====CMUSphinx1====#
			
			#file1.write('{}\n'.format(r.recognize_sphinx(audio_data = audio,language = (hmm,lm,dict1))))
			
			#print(r.recognize_sphinx(audio_data = audio,language = (hmm,lm,dict1)))
			#====CMUSphinx2====#
#			print(r.recognize_sphinx(audio_data = audio))
			#====Google Recognizer====#
			
			#file2.write('{}\n'.format(r.recognize_google(audio)))

			print(r.recognize_google(audio))
			bar.update(x+1)
			sleep(0.1)
			x += 1
bar.finish()

#file1.close()
#ßfile2.close()


