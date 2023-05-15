<!DOCTYPE html>
<html>
<head>
    <title>Загрузка и редактирование изображений</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/4.5.0/fabric.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@neptunian/react-photo-editor"></script>
    <script src="https://unpkg.com/resizerjs"></script>
</head>
<body>
    <h1>Загрузка и редактирование изображений</h1>
    <form method="POST" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file" accept="image/*">
        <input type="submit" value="Загрузить">
    </form>
    
    {% if file_url %}
        <h2>Ссылка на изображение:</h2>
        <a href="{{ file_url }}" target="_blank">{{ file_url }}</a>
        
        <h2>Редактировать изображение:</h2>
        <div id="canvas-container">
            <canvas id="canvas" width="400" height="300"></canvas>
        </div>
        <br>
        <button onclick="openEditor()">Изменить изображение</button>
    {% endif %}
    
    <script>
        var canvas = new fabric.Canvas('canvas');
        var imageObject = null;
        var editorInstance = null;

        function loadImage() {
            var fileInput = document.querySelector('input[type="file"]');
            var file = fileInput.files[0];
            var reader = new FileReader();
            reader.onload = function(event) {
                var imageUrl = event.target.result;
                fabric.Image.fromURL(imageUrl, function(img) {
                    canvas.clear();
                    canvas.add(img);
                    imageObject = img;
                });
            };
            reader.readAsDataURL(file);
        }

        function openEditor() {
            var fileInput = document.querySelector('input[type="file"]');
            if (fileInput.files.length === 0) {
                alert('Сначала загрузите изображение.');
                return;
            }

            var canvasContainer = document.getElementById('canvas-container');
            canvasContainer.style.display = 'none';

            editorInstance = new PhotoEditor(canvas, imageObject);
            editorInstance.open(function(updatedImage) {
                canvasContainer.style.display = 'block';
                canvas.clear();
                canvas.add(updatedImage);
                imageObject = updatedImage;
            });
        }

        function saveImage() {
            if (editorInstance) {
                var resizedImage = editorInstance.getImageScaledToCanvas();
                var file = ResizerJS.dataURLtoFile(resizedImage.toDataURL(), 'resized_image.png');

                var formData = new FormData();
                formData.append('file', file);

                fetch('/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    var fileUrl = data.file_url;
                    var linkElement = document.createElement('a');
                    linkElement.href = fileUrl;
                    linkElement.textContent = 'Ссылка на измененное изображение';
                    linkElement.target = '_blank';

                    var containerElement = document.getElementById('canvas-container');
                    containerElement.appendChild(linkElement);
                })
                .catch(error => {
                    console.error('Ошибка при сохранении изображения:', error);
                });
            }
        }
    </script>
</body>
</html>
