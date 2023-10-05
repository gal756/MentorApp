hljs.initHighlightingOnLoad();

var socket = io.connect('http://' + document.domain + ':' + location.port);

function sendMessage(event) {
    event.preventDefault(); // Prevent the form submission
    var message = document.getElementById('message-input').value;
    socket.emit('message', message); // Emit the message to the server
    document.getElementById('message-input').value = ''; // Clear the input field
}

socket.on('message', function(data) {
    var messageContainer = document.getElementById('message-container');
    var messageElement = document.createElement('div');
    messageElement.innerHTML = data.message;
    messageContainer.appendChild(messageElement);
});

var sharedCodeElement = document.getElementById('shared-code');

sharedCodeElement.addEventListener('input', function() {

    var selectionStart = sharedCodeElement.selectionStart;
    var selectionEnd = sharedCodeElement.selectionEnd;
    var sharedCode = sharedCodeElement.textContent;
    socket.emit('shared_code', sharedCode);
    sharedCodeElement.setSelectionRange(selectionStart, selectionEnd);
});

socket.on('shared_code', function(data) {

    var selectionStart = sharedCodeElement.selectionStart;
    var selectionEnd = sharedCodeElement.selectionEnd;
    sharedCodeElement.textContent = data.sharedCode;
    sharedCodeElement.setSelectionRange(selectionStart, selectionEnd);
    hljs.highlightAll();
    hljs.highlightBlock(sharedCodeElement);
});

function copyCode() {
    var codeElement = document.getElementById('shared-code');
    var textArea = document.createElement('textarea');
    textArea.value = codeElement.textContent;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    alert('Code copied to clipboard!');
}