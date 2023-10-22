from io import BytesIO
import os
from flask import Flask, render_template, request, Response, jsonify, send_file, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False
db_path = 'uploads.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

@app.route('/')
def hello_world():
    return render_template("upload.html")

ALLOWED_EXTENSIONS = ['mp4', 'mkv', 'mp3', 'png', 'jpg', 'jpeg']
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file found"
        file = request.files['file']
        if file.filename == '':
            return "No file selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_data = file.read()
            new_upload = Upload(filename=filename, data=file_data)
            db.session.add(new_upload)
            db.session.commit()
            return f'Uploaded {filename} successfully'
    return "invalid file type"

@app.route('/videos')
def display_images():
    video_records = Upload.query.filter(Upload.filename.like('%.mp4') | Upload.filename.like('%.mkv')).all()
    return render_template('videos.html', videos=video_records)

@app.route('/api/videos')
def display_videos():
    video_records = Upload.query.filter(Upload.filename.like('%.mp4') | Upload.filename.like('%.mkv')).all()
    
    # Convert the video_records to a list of dictionaries
    videos = [{'id': video.id, 'filename': video.filename} for video in video_records]
    
    return jsonify(videos=videos)


@app.route('/audios')
def display_audio():
    audio_records = Upload.query.filter(Upload.filename.like('%.mp3')).all()
    return render_template('audio.html', audios=audio_records)

@app.route('/get_video/<int:video_id>')
def get_video(video_id):
    video_record = Upload.query.filter_by(id=video_id).first()
    if video_record:
        return send_file(BytesIO(video_record.data),download_name=video_record.filename
        ,as_attachment=True)
    else:
        return "Video not found", 404

@app.route('/get_audio/<int:audio_id>')
def get_audio(audio_id):
    audio_record = Upload.query.get(audio_id)

    if audio_record:
        response = Response(audio_record.data, content_type='audio/mp3')  # Adjust content_type as needed
        return response
    else:
        return "Audio not found", 404

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists(db_path):
            db.create_all()
    app.run(host='0.0.0.0', debug=True)