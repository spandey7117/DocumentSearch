from flask import Flask, render_template, send_from_directory, request, g
from dotenv import find_dotenv, load_dotenv
import os

from chatGPTIntegration import read_pdf, read_doc, read_txt, respond_to_query

load_dotenv(find_dotenv())
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    file_path = ''
    try:
        if 'fileInput' not in request.files:
            is_upload_success = False
            message = "Please select correct file"
            return render_template('upload.html', message=message, is_upload_success=is_upload_success)

        file = request.files['fileInput']
        if file.filename == '':
            is_upload_success = False
            message = "No selected file"
            return render_template('upload.html', message=message, is_upload_success=is_upload_success)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        message = "File uploaded successfully to: " + file_path
        is_upload_success = True
    except Exception as e:
        message = "File uploaded Failed, Please try again."
        is_upload_success = False
    finally:
        return render_template('upload.html', message=message, is_upload_success=is_upload_success, file_path=file_path)


def get_response_from_file(human_input):
    pass


@app.route('/send_message', methods=['POST'])
def send_message():
    human_input = request.form['human_input']
    file_path = request.form['file_path']
    file_type = file_path.split('.')[2]
    print('file_type', file_type)
    if file_type == 'pdf':
        raw_text = read_pdf(file_path)
    elif file_type == 'doc' or file_type == 'docx':
        raw_text = read_doc(file_path)
    else:
        raw_text = read_txt(file_path)
    response_from_llm = respond_to_query(raw_text, human_input)

    return render_template('upload.html', is_upload_success=True, file_path=file_path,
                           response_from_llm=response_from_llm)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
