from flask import Flask, render_template
from flask import send_from_directory
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# UNCOMMENT ME
# from actual import main

# DELETE ME
def main(arg1, arg2, arg3):
    print('doing nothing')

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

@app.route('/em', methods=['GET', 'POST'])
def em():
    if request.method == 'POST':
        # check if the post request has the file part
        text = request.files['text']
        template = request.files['template']
        addresses = request.files['addresses']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        filename_text = secure_filename(text.filename)
        text.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_text))

        filename_template = secure_filename(template.filename)
        template.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_template))

        filename_addresses = secure_filename(addresses.filename)
        addresses.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_addresses))

        main(filename_text, filename_template, filename_addresses)
        return redirect('/em')
    return render_template('em.html')

@app.route('/wa')
def wa():
    return render_template('wa.html')

@app.route('/')
def index():
    return render_template('index.html')
