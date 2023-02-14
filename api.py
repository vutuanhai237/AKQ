from PIL import Image
from flask import Flask, flash, redirect, jsonify, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from os import path
from shutil import copyfile
import io, glob, base64, shutil, os.path, time
from flask_ngrok import run_with_ngrok
app = Flask('image_encrypt')
app.config['UPLOAD_FOLDER'] = 'images'
CORS(app)
# run_with_ngrok(app)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
fileName = ''


def uploadFile():
    f = request.files['file']
    global fileName
    fileName = f.filename[0:-4]
    f.save(os.path.join(app.config['images'], f.filename))
    return
@app.route('/test', methods=['GET'])
def getVideo():
    """Download a file."""
    return 'aaa'
app.run()