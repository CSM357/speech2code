const startButton = document.getElementById('startButton');
const translateButton = document.getElementById('translateButton');
const inputTextarea = document.getElementById('input');
const outputDiv = document.getElementById('output');
let recognition;

startButton.addEventListener('click', () => {
    startButton.disabled = true;
    inputTextarea.disabled = true;
    outputDiv.textContent = 'Listening...';
    try {
        recognition = new webkitSpeechRecognition();
        recognition.lang = 'en-US';
        recognition.start();

        recognition.onresult = (event) => {
            const result = event.results[0][0].transcript;
            inputTextarea.value = result;
            outputDiv.textContent = 'Speech recognized. Click "Convert" to proceed.';
            recognition.stop();
        };

        recognition.onerror = (event) => {
            console.error('Recognition error:', event.error);
            outputDiv.textContent = 'Error: Recognition failed.';
        };
    } catch (error) {
        console.error('Error starting speech recognition:', error);
        outputDiv.textContent = 'Error: Speech recognition not supported.';
    }
});

translateButton.addEventListener('click', () => {
    const command = inputTextarea.value;
    outputDiv.textContent = 'Converting...';

    fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        outputDiv.textContent = data.code_output;
    })
    .catch(error => {
        console.error('Error:', error);
        outputDiv.textContent = 'Error: Unable to convert. Please try again later.';
    });
});