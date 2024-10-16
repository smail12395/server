from flask import Flask, request, jsonify, send_from_directory, url_for
import os
import uuid

app = Flask(__name__)

# مسار المجلد المؤقت
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/notify', methods=['GET'])
def notify():
    return jsonify({'message': 'Server notified successfully!'})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # إنشاء اسم فريد للملف لحفظه مؤقتًا
    unique_filename = str(uuid.uuid4()) + "_" + file.filename
    temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    
    # حفظ الملف في المجلد المؤقت
    file.save(temp_file_path)

    # إنشاء رابط تحميل مؤقت للصورة
    download_url = url_for('download_file', filename=unique_filename, _external=True)
    
    return jsonify({'message': 'File uploaded successfully!', 'download_url': download_url}), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # التأكد من وجود الملف في المجلد المؤقت
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
