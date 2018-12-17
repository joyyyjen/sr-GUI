from definition import CFG
import os


def check_extension_name(fp: str) -> bool:
    ext_name = os.path.splitext(fp)[1].lower()
    if ext_name in CFG["ALLOWED_EXTENSIONS"]:
        return True
    return False
