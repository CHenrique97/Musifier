import flask
from flask import request, jsonify
import os
app = flask.Flask(__name__)
app.config["DEBUG"] = True



@app.route('/', methods=['GET'])
def home():
    os.system('cmd /c "python composer.py"')
    return {'fileLocation': "ftp://localhost:21/song.mid"}




app.run()