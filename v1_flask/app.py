import os
import cv2
import base64
import numpy as np
from flask import Flask, render_template, request, jsonify
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
profil_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/capture', methods=['POST'])
def capture():
    data = request.get_json()
    image_data = data['image']
    return jsonify({'status': 'success', 'message': 'Image received successfully'})

@sock.route('/video_feed')
def video_feed(ws):
    frame_count = 0
    while True:
        data = ws.receive()
        frame = base64.b64decode(data)
        frame = np.frombuffer(frame, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        frame_count += 1
        if frame_count % 3 != 0:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(25, 25))
        profils = profil_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))

        rectangles = []
        
        for (x, y, w, h) in faces:
            blur_radius = int(max(w, h) / 14)
            if blur_radius % 2 == 0:
                blur_radius += 1
            blurred_face = cv2.GaussianBlur(frame[y:y+h, x:x+w], (blur_radius, blur_radius), 0)
            frame[y:y+h, x:x+w] = blurred_face

            for _ in range(int(((w * w) / 160 - w / 2))):
                rx = np.random.randint(x, x + w)
                ry = np.random.randint(y, y + h)
                rwidth = np.random.randint(2, 20)
                rheight = np.random.randint(2, 20)
                pastel_color = np.random.randint(150, 256, size=(3,), dtype=np.uint8)
                rectangles.append({
                    'x': rx, 'y': ry, 'width': rwidth, 'height': rheight,
                    'color': pastel_color.tolist()
                })

        for (x, y, w, h) in profils:
            for _ in range(int(((w * w) / 160 - w / 2))):
                rx = np.random.randint(x, x + w)
                ry = np.random.randint(y, y + h)
                rwidth = np.random.randint(2, 20)
                rheight = np.random.randint(2, 20)
                pastel_color = np.random.randint(150, 256, size=(3,), dtype=np.uint8)
                rectangles.append({
                    'x': rx, 'y': ry, 'width': rwidth, 'height': rheight,
                    'color': pastel_color.tolist()
                })

        for _ in range(64):
            rx = np.random.randint(0, frame.shape[1])
            ry = np.random.randint(0, frame.shape[0])
            rwidth = np.random.randint(2, 100)
            rheight = np.random.randint(2, 100)
            pastel_color = np.random.randint(150, 256, size=(3,), dtype=np.uint8)
            rectangles.append({
                'x': rx, 'y': ry, 'width': rwidth, 'height': rheight,
                'color': pastel_color.tolist()
            })

        ws.send(json.dumps({'rectangles': rectangles}))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
