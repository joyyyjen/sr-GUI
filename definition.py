import os
import yaml

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
INSTANCE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance")
SITE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flask_site")
UPLOAD_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "upload")

cfg_files = [
    os.path.join(INSTANCE_ROOT, "test.YAML")
]

CFG_FPATH = [fpath for fpath in cfg_files if os.path.isfile(fpath)][-1]
CFG = {}

with open(CFG_FPATH, mode="r") as f:
    CFG.update(yaml.load(f))
