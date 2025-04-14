from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# إعداد مجلد رفع الصور
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# السماح بامتدادات الصور
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return "🚀 السيرفر يعمل - Flask على Render"

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "الرجاء إرسال ملف صورة باسم image"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "اسم الملف فارغ"}), 400

    if image and allowed_file(image.filename):
        # تأمين الاسم + إضافة توقيت لتفادي التكرار
        filename = secure_filename(image.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        final_name = f"{timestamp}_{filename}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], final_name)
        image.save(save_path)

        # توليد الرابط المباشر
        image_url = request.host_url + 'static/uploads/' + final_name
        return jsonify({"message": "✅ تم رفع الصورة", "url": image_url}), 200

    return jsonify({"error": "امتداد الملف غير مدعوم"}), 400
