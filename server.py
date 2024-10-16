from flask import Flask, request, jsonify
import os
import tempfile

app = Flask(__name__)

@app.route('/notify', methods=['GET'])
def notify():
    # إشعار بسيط بأن التطبيق قد بدأ
    return "Application started successfully", 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400
    
    # تخزين الملف في مجلد tmp مؤقتًا
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)
    
    # هنا يتم إنشاء رابط التحميل (وهو رابط مؤقت فقط للسياق الحالي)
    # في بيئة production ستحتاج لإعداد خادم لتحميل الملفات
    download_url = f"http://server-omh1.onrender.com/download/{file.filename}"
    
    return jsonify({
        "message": f"File {file.filename} uploaded successfully",
        "download_url": download_url
    }), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # استرجاع الملف من tmp وإرساله كاستجابة للتحميل
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    
    if os.path.exists(file_path):
        return app.send_static_file(file_path)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
