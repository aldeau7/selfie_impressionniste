const background = document.getElementById('background');

// Function to generate a random number within a range
function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Function to generate a random pastel color with transparency
function getRandomPastelColor() {
    const r = getRandomNumber(150, 255);
    const g = getRandomNumber(150, 255);
    const b = getRandomNumber(150, 255);
    const alpha = Math.random() * (0.5 - 0.2) + 0.2; // Adjust the range for transparency
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

// Function to create a rectangle and add it to the background
function createRectangle() {
    const rectangle = document.createElement('div');
    rectangle.classList.add('rectangle');
    rectangle.style.top = `${getRandomNumber(0, window.innerHeight)}px`;
    rectangle.style.left = `${getRandomNumber(0, window.innerWidth)}px`;
    rectangle.style.backgroundColor = getRandomPastelColor(); // Set random pastel color with transparency
    background.appendChild(rectangle);
}

// Set background image with transparency
background.style.backgroundImage = "url('static/test1.jpg')";
background.style.backgroundSize = 'cover'; // Adjust as needed
background.style.backgroundPosition = 'center'; // Adjust as needed

// Create rectangles periodically
setInterval(createRectangle, 100); // Adjust timing as needed
