from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from PIL import Image
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Specify the directory to save the uploaded files
UPLOAD_DIRECTORY = 'uploads'
RESULT_DIRECTORY = 'static/results'

# Route to render the home page
@app.route('/')
def home():
    processed_file = session.get('processed_file')
    output = session.get('output')
    session.pop('processed_file', None)  # Remove the session variable
    session.pop('output', None)  # Remove the session variable

    options = load_options()
    # print(options)
    return render_template('index.html', options=options, processed_file=processed_file, output=output)

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload():
    file_processing()
    # print(subprocess.run(["./c++/model"],capture_output=True).stdout.decode("utf-8")) # ,stdout=PIPE

    return redirect(url_for('home'))

# Load options from the configuration file
def load_options():
    with open('config.json') as f:
        config = json.load(f)
    return config['options']

def file_processing():
    if 'file' not in request.files:
        return redirect(request.url)
    # print(request.form.get('ml-task'))
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    file_name = file.filename

    # Create the uploads directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    
    # Save the uploaded file to the uploads directory
    new_file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    file.save(new_file_path)

    if not os.path.exists(RESULT_DIRECTORY):
        os.makedirs(RESULT_DIRECTORY)

    image = Image.open(new_file_path)


    # Mimic processing 
    # TODO add thread.sleep(2000ms)
    # Rotate the image by a specific angle (in degrees)
    angle = 90
    rotated_image = image.rotate(angle)

    # Save the rotated image
    result_file_path = os.path.join(RESULT_DIRECTORY, 'abc.png')
    rotated_image.save(result_file_path)
    
    # Store the result file path and output as session variables
    session['processed_file'] = result_file_path
    session['output'] = True

if __name__ == '__main__':
    app.run(debug=True)
    