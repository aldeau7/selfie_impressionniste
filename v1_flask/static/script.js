const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
let frameCounter = 0;
let rectangles = [];

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        video.addEventListener('loadedmetadata', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerWidth * (video.videoHeight / video.videoWidth);
            requestAnimationFrame(sendFrame);
        });
    })
    .catch(err => {
        console.error("Error accessing the camera: " + err);
    });

const ws = new WebSocket('ws://' + window.location.host + '/video_feed');

ws.onopen = () => {
    console.log('WebSocket connection opened');
};

ws.onmessage = event => {
    const data = JSON.parse(event.data);
    rectangles = data.rectangles;
    drawFrame();
};

ws.onerror = error => {
    console.error("WebSocket error: " + error);
};

function sendFrame() {
    if (frameCounter % 5 === 0) {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL('image/jpeg');
        const base64 = dataUrl.split(',')[1];
        //ws.send(base64);
    }
    frameCounter++;
    requestAnimationFrame(sendFrame);
}

function drawFrame() {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    rectangles.forEach(rect => {
        context.fillStyle = `rgba(${rect.color[0]}, ${rect.color[1]}, ${rect.color[2]}, 0.5)`;
        context.fillRect(rect.x, rect.y, rect.width, rect.height);
    });
}

captureButton.addEventListener('click', () => {
    const dataUrl = canvas.toDataURL('image/jpeg');
    const link = document.createElement('a');
    link.href = dataUrl;
    link.download = 'capture.jpeg';
    link.click();
});
