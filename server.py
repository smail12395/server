from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# إعداد مسار حفظ الصور المرفوعة
UPLOAD_FOLDER = 'uploaded_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# إعداد البريد الإلكتروني
EMAIL_ADDRESS = os.getenv('smailkindle4@gmail.com')  # احصل على البريد الإلكتروني من متغيرات البيئة
EMAIL_PASSWORD = os.getenv('smail123!!')  # احصل على كلمة المرور من متغيرات البيئة
RECIPIENT_EMAIL = 'smailtaafyy55@gmail.com'  # البريد الإلكتروني المستلم (يمكن تغييره)

# إرسال الصور بالبريد الإلكتروني
def send_email_with_attachment(file_path, filename):
    msg = EmailMessage()
    msg['Subject'] = 'New Image Uploaded'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg.set_content(f"A new image '{filename}' has been uploaded.")

    # إضافة المرفق
    with open(file_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=filename)

    # إرسال البريد الإلكتروني
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

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
    
    # حفظ الملف في المجلد
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # إرسال الملف عبر البريد الإلكتروني
    try:
        send_email_with_attachment(file_path, file.filename)
        return jsonify({'message': 'File uploaded and sent via email successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
