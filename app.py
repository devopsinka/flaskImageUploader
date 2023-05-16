from flask import Flask, request, render_template, redirect, url_for, send_from_directory, session
from transliterate import translit
from captcha.image import ImageCaptcha
import os
import random


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Устанавливаем папку для загрузки файлов
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    # Проверяем разрешенное расширение файла
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def transliterate_filename(filename):
    base, ext = os.path.splitext(filename)
    transliterated_base = translit(base, 'ru', reversed=True)
    transliterated_filename = transliterated_base.lower().replace(' ', '_') + ext
    return transliterated_filename


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            filename = transliterate_filename(filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            file_url = url_for('uploaded_file', filename=filename, _external=True)
            return render_template('index.html', file_url=file_url)
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Проверяем, что файл был отправлен в запросе
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    # Проверяем, что файл имеет допустимое расширение
    if file and allowed_file(file.filename):
        # Проверяем правильность Captcha
        user_captcha = request.form.get('captcha', '').upper()
        captcha_text = session.get('captcha_text', '')
        if user_captcha != captcha_text:
            return render_template('index.html', error='Неверная Captcha', captcha_text=captcha_text)
        
        # Сохраняем файл в папку uploads
        filename = file.filename
        filename = transliterate_filename(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Создаем ссылку на загруженный файл
        file_url = url_for('uploaded_file', filename=filename, _external=True)
        
        # Возвращаем главную страницу с ссылкой на загруженное изображение
        return render_template('index.html', file_url=file_url)
    
    # Если файл имеет недопустимое расширение или Captcha неправильная,
    # перенаправляем пользователя обратно на форму загрузки с сообщением об ошибке
    return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Отображаем загруженный файл
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run()
