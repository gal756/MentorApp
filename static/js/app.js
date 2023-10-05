document.addEventListener('DOMContentLoaded', (event) => {
    hljs.highlightAll();

    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var sharedCodeElement = document.getElementById('shared-code');

    sharedCodeElement.addEventListener('input', function() {
        socket.emit('shared_code', { sharedCode: sharedCodeElement.textContent });
    });

    socket.on('shared_code', function(data) {
        sharedCodeElement.textContent = data.sharedCode;
        hljs.highlightBlock(sharedCodeElement);
        // Ensure the text direction remains left-to-right
        sharedCodeElement.style.direction = 'ltr';
    });
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
