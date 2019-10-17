import os
from flask import Flask, render_template, request
from flask_cors import CORS

# import our OCR function
from OCR import ocr_core

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
CORS(app, support_credentials=True)


# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@app.route('/')
def home_page():
    #return render_template('index.html')
    return "Got it", 200

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # TODO: Handle no-file exceptions
        file = request.data
        print(file)
        # call the OCR function on it
        extracted_text = ocr_core(file)

        if len(extracted_text) == 0:
            extracted_text = "No text found, sorry!"

        return extracted_text, 200
        # extract the text and display it
        # return render_template('upload.html',
        #                        msg='Successfully processed',
        #                        extracted_text=extracted_text,
        #                        img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')