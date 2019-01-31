#!/usr/local/bin/python3

import speech_recognition as sr
import os
from sr_anlz.definition import PKG_DIR

def recognition():

    r = sr.Recognizer()
    output_path  =  os.path.join(PKG_DIR,"output", "recognition.txt")
    file1 = open(output_path, 'w+')
    id_path = os.path.join(PKG_DIR,"refined-audio", "fileid.txt")
    audio_path = os.path.join(PKG_DIR,"refined-audio/")
    with open(id_path, 'r') as f:
        for id in f:
            path = audio_path + id.strip('\n') + ".wav"
            AudioCollection = sr.AudioFile(path)
            with AudioCollection as source:
                audio = r.record(source)
                # ====Google Speech Recognizer====#
                file1.write('{}\n'.format(r.recognize_google(audio)))
        # print(r.recognize_google(audio))

    file1.close()
