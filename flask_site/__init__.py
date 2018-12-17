from flask import Flask, render_template, request
from definition import CFG, SITE_ROOT, UPLOAD_ROOT
from sr_anlz.execute.main import execute
import flask_site.utility as uti
import os

app = Flask(__name__, instance_relative_config=True)


@app.route("/", methods=["GET", "POST"])
def index():
    # POST
    if request.method == "POST":
        file = request.files['file']
        fp = os.path.join(UPLOAD_ROOT, file.filename)
        file.save(fp)
        # Process Data and Output
        # OPT
        OPT = execute(fp)
        # TXT
        with open(OPT[0], mode="r") as f:
            TXT = f.read()
        # PIE
        PIE_DATA = [["Error_Type", "Error_Count"]]

        PIE_DATA.extend([[i[0], i[1][0]] for i in OPT[1] if i[0] != "WER"])
        # return
        return render_template("index.html", CFG=CFG, OPT=OPT[1], TXT_REPORT=TXT, PIE_DATA=PIE_DATA)
    # GET
    return render_template("index.html", CFG=CFG)


@app.errorhandler(404)
def not_found(error):
    return render_template("index.html", CFG=CFG, OPT={})
    # return render_template("page_404.html", ERR=error), 404
