from flask_site import app
from definition import CFG, CFG_FPATH

if __name__ == "__main__":
    print(" * CFG PATH:", CFG_FPATH)
    app.run(debug=CFG["DEBUG"])
