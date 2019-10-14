#!flask/bin/python
from flask import Flask
import os
import sys
import shutil
from flask import request
from common import *
sys.path.append("./darkflow/")
from script import predict


app = Flask(__name__)

@app.route('/<method>')
def index(method):
    shutil.rmtree(os.getcwd() + "/frames")
    shutil.rmtree(os.getcwd() + "/output-images")
    os.mkdir("./frames")
    os.mkdir("./output-images")

    videoPath = request.headers.get('video-path')
    print("video path = " + videoPath)
    FrameCapture(str(videoPath))
    if method == "yolo":
        print("method = " + method)
        return predict(videoPath)
    else:
        return "Hello, World!"


if __name__ == '__main__':

    app.run(debug=True)
