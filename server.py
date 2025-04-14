from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# مجلد حفظ الصور
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return "Server is running..."

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "لم يتم إرسال صورة"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "اسم الملف فارغ"}), 400

    # إنشاء اسم آمن وفريد للملف
    filename = secure_filename(image.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    final_name = f"{timestamp}_{filename}"
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], final_name)
    image.save(image_path)

    # رابط الوصول للصورة
    image_url = request.host_url + 'static/uploads/' + final_name
    return jsonify({"message": "تم الحفظ", "url": image_url}), 200

# لتشغيل محليًا فقط
# if __name__ == '__main__':
#     app.run(debug=True)
