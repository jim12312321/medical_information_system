import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

# Custom import modules
from stt import speech_to_text

UPLOAD_FOLDER = "./upload"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = (1024 * 1024 * 32)

@app.route("/")
def index():
    return "index"

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            response = speech_to_text(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return_dict = {}
            return_dict["result"] = ""
            return_dict["source_stt"] = response
            return_dict["source"] = url_for("get_recording", filename=filename, _external=True)
            return_dict["responseMedia"] = ""
            return return_dict
    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file>
            <input type=submit value=Upload>
        </form>
        '''

@app.route('/files/res/<filename>')
def get_response(filename):
    return 'foo'

@app.route('/files/rec/<filename>')
def get_recording(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, host='10.121.148.135', port=5000)