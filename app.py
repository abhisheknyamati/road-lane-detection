# from flask import Flask, render_template, request, send_file
# import os
# from moviepy.editor import VideoFileClip
# from line_fit_video import annotate_video

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# OUTPUT_FOLDER = 'outputs'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/annotate', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return "No file part"

#     file = request.files['file']
#     if file.filename == '':
#         return "No selected file"

#     if file:
#         filename = file.filename
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)

#         output_file = os.path.join(app.config['OUTPUT_FOLDER'], 'annotated_' + filename)
#         annotate_video(file_path, output_file)

#         return send_file(output_file, as_attachment=True)


# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, send_file, url_for
import os
from moviepy.editor import VideoFileClip
from line_fit_video import annotate_video

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


@app.route('/')
def index():
    return render_template('index.html', processed_file=None)


@app.route('/annotate', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        output_file = os.path.join(app.config['OUTPUT_FOLDER'], 'annotated_' + filename)
        print("output file: ", output_file)
        annotate_video(file_path, output_file)
        print("output file: ", output_file)
        # return render_template('index.html', processed_file=output_file)

        return render_template('index.html', processed_file = url_for('static', filename='outputs/annotated_' + filename))
if __name__ == '__main__':
    app.run(debug=True)
