from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# تحديد مجلد ثابت لحفظ الصور
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/notify', methods=['GET'])
def notify():
    return "Application started successfully", 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400
    
    # حفظ الملف في مجلد ثابت
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # إنشاء رابط تحميل للملف
    download_url = f"https://server-omh1.onrender.com/download/{file.filename}"
    
    return jsonify({
        "message": f"File {file.filename} uploaded successfully",
        "download_url": download_url
    }), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # خدمة الملفات من المجلد الثابت
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
