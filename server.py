from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

app = Flask(__name__)

# إعدادات البريد الإلكتروني
EMAIL_ADDRESS = 'smailkindle4@gmail.com'  # استبدلها ببريدك الإلكتروني
EMAIL_PASSWORD = 'smail123!!'     # استبدلها بكلمة مرور بريدك الإلكتروني

def send_email(file_path):
    # إعداد البريد الإلكتروني
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS  # يمكنك تغيير هذا إلى بريد إلكتروني مختلف
    msg['Subject'] = 'تم رفع صورة جديدة'
    
    # إعداد ملف الصورة كمرفق
    attachment = MIMEBase('application', 'octet-stream')
    with open(file_path, 'rb') as file:
        attachment.set_payload(file.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
    msg.attach(attachment)

    # إرسال البريد الإلكتروني
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # تفعيل التشفير
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f'Email sent successfully with attachment {file_path}')
    except Exception as e:
        print(f'Failed to send email: {e}')

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
    
    # حفظ الملف مؤقتًا
    temp_file_path = os.path.join('/tmp', file.filename)
    file.save(temp_file_path)

    # إرسال البريد الإلكتروني
    send_email(temp_file_path)

    # حذف الملف المؤقت
    os.remove(temp_file_path)

    return jsonify({'message': 'File uploaded and emailed successfully!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
