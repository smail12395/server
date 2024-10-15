from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# إعداد مسار حفظ الصور المرفوعة
UPLOAD_FOLDER = 'uploaded_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({'message': 'File uploaded successfully!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)