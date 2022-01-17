import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

# Custom import modules
from stt import speech_to_text
from tts import hash_sha256, text_to_speech
from utils import resp_json_gen, respond_decide

UPLOAD_FOLDER = "./upload"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = (1024 * 1024 * 32)

@app.route("/")
def index():
    return "index"

@app.route('/upload/<senario>', methods=['GET', 'POST'])
def upload(senario):
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            source_text = speech_to_text(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            respond = respond_decide(source_text)
            respond_media = text_to_speech(respond)


            return_dict = resp_json_gen(respond, url_for("get_recording", filename=filename, _external=True),
                                            source_text, url_for("get_response", filename=respond_media, _external=True))
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
    return send_from_directory('./response/', filename)

@app.route('/files/rec/<filename>')
def get_recording(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)