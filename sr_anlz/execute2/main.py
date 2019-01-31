#!/usr/local/bin/python3
import zipfile
import os
import shutil
from sr_anlz.definition import PKG_DIR
from sr_anlz.execute2.recognizer import recognition
from sr_anlz.execute2.freq import main_freq, sec_freq

def clean():
    path_to_clean = os.path.join(PKG_DIR, "output")
    print("CleanOutput")
    for filename in os.listdir(path_to_clean):
        print(filename)
        #file_path = os.path.join(path_to_clean,filename)
        #os.unlink(file_path)


def execute(zip_file):
    clean()
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(PKG_DIR)

    basename = os.path.basename(zip_file).split(".")[0]

    audio_path_before = os.path.join(PKG_DIR, basename)
    audio_path = os.path.join(PKG_DIR, "refined-audio")

    if os.path.isdir(audio_path):
        shutil.rmtree(audio_path)

    os.rename(audio_path_before, audio_path)
    print("Start Recognition")
    recognition()
    print("Start Analyzing")
    result_fp, result = main_freq()

    return result_fp, result


def analyze(rf,tf):
    clean()
    print("Start Analyzing")
    result_fp, result = sec_freq(rf,tf)
    return result_fp, result

