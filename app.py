from flask import Flask, flash, redirect, render_template, request, send_file, url_for
import os
from moviepy.editor import VideoFileClip
from line_fit_video import annotate_video
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'

@app.route('/')
def index():
    return render_template('index.html', processed_file=None)


@app.route('/annotate', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_file_path)

        # Assuming you have an `outputs` folder within `static` where processed videos are stored
        output_filename = 'annotated_' + filename
        output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        # Process the video
        annotate_video(input_file_path, output_file_path)

        # Generate URL paths for the input and output videos
        input_url = url_for('static', filename='uploads/' + filename)
        output_url = url_for('static', filename='outputs/' + output_filename)

        return render_template('index.html', input_file=input_url, processed_file=output_url)

    return redirect(url_for('index'))  # Assuming you have a route and template for 'index'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4'}

if __name__ == '__main__':
    app.run(debug=True)
