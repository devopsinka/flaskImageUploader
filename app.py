from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Устанавливаем папку для загрузки файлов
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    # Проверяем разрешенное расширение файла
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Отображаем форму загрузки файла
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Проверяем, что файл был отправлен в запросе
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    # Проверяем, что файл имеет допустимое расширение
    if file and allowed_file(file.filename):
        # Сохраняем файл в папку uploads
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Создаем ссылку на загруженный файл
        file_url = url_for('uploaded_file', filename=filename, _external=True)
        
        # Возвращаем главную страницу с ссылкой на загруженное изображение
        return render_template('index.html', file_url=file_url)
    
    # Если файл имеет недопустимое расширение, перенаправляем пользователя обратно на форму загрузки
    return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Отображаем загруженный файл
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run()
