#!/usr/local/bin/python3
import zipfile
import os
import shutil
from sr_anlz.definition import PKG_DIR
from sr_anlz.execute.recognizer import recognition
from sr_anlz.execute.freq import main_freq

'''
if len(sys.argv) != 2:
    print("Usage: {} zipfile".format(sys.argv[0]))
    sys.exit(1)
'''


def execute(zip_file):
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


