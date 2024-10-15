from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# إعدادات البريد الإلكتروني
EMAIL_USER = 'smailkindle4@gmail.com'
EMAIL_PASSWORD = 'smail123!!'
EMAIL_RECEIVER = 'smailtaafyy55@gmail.com'

# وظيفة إرسال البريد الإلكتروني مع المرفق
def send_email_with_attachment(file_path, filename):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = 'New File Uploaded'

    body = 'A new file has been uploaded.'
    msg.attach(MIMEText(body, 'plain'))

    # إضافة المرفق
    attachment = open(file_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {filename}')
    msg.attach(part)

    # إعداد خادم SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_USER, EMAIL_RECEIVER, text)
    server.quit()

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # حفظ الملف مؤقتاً في مجلد محلي
        temp_folder = 'temp_uploads'
        os.makedirs(temp_folder, exist_ok=True)
        file_path = os.path.join(temp_folder, file.filename)
        file.save(file_path)

        # إرسال الملف عبر البريد الإلكتروني
        send_email_with_attachment(file_path, file.filename)

        # حذف الملف بعد الإرسال
        os.remove(file_path)

        return jsonify({'message': 'File uploaded and sent via email successfully!'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to upload and send file: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

