#!/usr/local/bin/python3
import zipfile
import os
import shutil
from sr_trng.definition import PKG_DIR
from sr_trng.execute.scriptPreprocess import script
from sr_trng.execute.CatchTrainWarning import catch
import subprocess

def clean(dir_name):
    path_to_clean = os.path.join(PKG_DIR, dir_name)
    print("CleanOutput")
    for filename in os.listdir(path_to_clean):
        print(filename)
        file_path = os.path.join(path_to_clean,filename)
        os.unlink(file_path)


def execute(zip_file):
    clean('output')

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(PKG_DIR)

    basename = os.path.basename(zip_file).split(".")[0]

    audio_path_before = os.path.join(PKG_DIR, basename)
    audio_path = os.path.join(PKG_DIR, "model-directory")

    clean('model-directory')

    os.rename(audio_path_before, audio_path)

    script()
    pass_arg = []
    pass_arg.append(os.path.join(PKG_DIR, "execute",'adapt.sh'))
    # Unzip File Path
    pass_arg.append(os.path.join(PKG_DIR, "model-directory"))
    # Training File Path
    pass_arg.append(os.path.join(PKG_DIR, "training-functions"))
    # Output File Path
    pass_arg.append(os.path.join(PKG_DIR, "output"))
    # New Model File Path
    pass_arg.append(os.path.join(PKG_DIR, "output","model-adapt"))
    pass_arg2 = []
    #pass_arg2.append('mkdir')
    #pass_arg2.append(os.path.join(PKG_DIR, "model-directory","model-adapt"))
    #os.system(' '.join(pass_arg2))
    subprocess.check_call(pass_arg)
    errors = catch()

    shutil.make_archive('output', 'zip', root_dir=os.path.join(PKG_DIR, "output"))
    shutil.move('output.zip',os.path.join(PKG_DIR, "model-directory"))
    fp = os.path.join(PKG_DIR, "model-directory","output.zip")
    return fp,errors



    #result_fp, result = main_freq()

    #return result_fp, result


def analyze(rf,tf):
    clean()
    print("Start Analyzing")
    result_fp, result = sec_freq(rf,tf)
    return result_fp, result
