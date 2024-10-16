from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# المسار المؤقت لحفظ الملفات
TEMP_UPLOAD_FOLDER = '/tmp'

# تأكد من أن المجلد موجود
if not os.path.exists(TEMP_UPLOAD_FOLDER):
    os.makedirs(TEMP_UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # حفظ الملف مؤقتًا في مجلد /tmp
    file_path = os.path.join(TEMP_UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # إرسال رابط لتحميل الملف
    return jsonify({
        'message': 'File uploaded successfully!',
        'download_link': f'/download/{file.filename}'
    }), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # إرسال الملف من مجلد /tmp
    return send_from_directory(TEMP_UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
