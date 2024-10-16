from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import logging
import dotenv  # تأكد من تثبيت مكتبة python-dotenv

# تحميل متغيرات البيئة من ملف .env
dotenv.load_dotenv()

app = Flask(__name__)

# إعدادات تسجيل الأخطاء
logging.basicConfig(level=logging.DEBUG)

# إعدادات البريد الإلكتروني
EMAIL_ADDRESS = os.getenv('smailkindle4@gmail.com')  # احصل على البريد الإلكتروني من متغير البيئة
EMAIL_PASSWORD = os.getenv('smail123!!')  # احصل على كلمة المرور من متغير البيئة

# تأكيد أن بيانات البريد الإلكتروني تم تحميلها
if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    logging.error('Email credentials are not properly set in the environment variables.')

def send_email(file_path, recipient=EMAIL_ADDRESS, subject='تم رفع صورة جديدة'):
    logging.info('Preparing to send email with attachment: %s', file_path)
    
    # إعداد البريد الإلكتروني
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient
    msg['Subject'] = subject
    
    # إعداد ملف الصورة كمرفق
    try:
        attachment = MIMEBase('application', 'octet-stream')
        with open(file_path, 'rb') as file:
            attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
        msg.attach(attachment)
        logging.info('Attachment added successfully: %s', file_path)

        # إرسال البريد الإلكتروني
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # تفعيل التشفير
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            logging.info('Email sent successfully to: %s', recipient)
    except FileNotFoundError:
        logging.error('File not found: %s', file_path)
    except smtplib.SMTPAuthenticationError:
        logging.error('SMTP Authentication Error: Check email credentials.')
    except Exception as e:
        logging.error('Failed to send email: %s', e)

@app.route('/notify', methods=['GET'])
def notify():
    logging.info('Notify endpoint hit')
    return jsonify({'message': 'Server notified successfully!'})

@app.route('/upload', methods=['POST'])
def upload_file():
    logging.info('Upload endpoint hit')
    
    if 'file' not in request.files:
        logging.error('No file part in the request')
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        logging.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    # تحقق من نوع الملف
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        logging.error('Invalid file type: %s', file.filename)
        return jsonify({'error': 'Invalid file type. Only image files are allowed.'}), 400
    
    # حفظ الملف مؤقتًا
    temp_file_path = os.path.join('/tmp', file.filename)
    try:
        logging.info('Saving file temporarily to: %s', temp_file_path)
        file.save(temp_file_path)
        
        # إرسال البريد الإلكتروني
        logging.info('File saved successfully. Now sending email.')
        send_email(temp_file_path)
    except Exception as e:
        logging.error('Failed to save file or send email: %s', e)
        return jsonify({'error': f'Failed to save file or send email: {e}'}), 500
    finally:
        # حذف الملف المؤقت
        if os.path.exists(temp_file_path):
            logging.info('Removing temporary file: %s', temp_file_path)
            os.remove(temp_file_path)

    logging.info('File uploaded and emailed successfully.')
    return jsonify({'message': 'File uploaded and emailed successfully!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

