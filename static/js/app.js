document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('save-btn').addEventListener('click', function() {
      checkCode();
  });
});

function normalizeCode(code) {
    // Remove all whitespace characters and convert to lowercase
    return code.replace(/\s+/g, '').toLowerCase();
}

function checkCode() {
    // Get the solution from the data-solution attribute
    var solutionCode = document.getElementById('save-btn').getAttribute('data-solution');
    var userCode = document.getElementById('editing').value;

    // Normalize the code strings
    var normalizedUserCode = normalizeCode(userCode);
    var normalizedSolutionCode = normalizeCode(solutionCode);
    if(normalizedUserCode === normalizedSolutionCode) {
        alert("Correct! 😊");
    } else {
        alert("Try again! 😕");
    }
}


function update(text) {
  let result_element = document.querySelector("#highlighting-content");
  result_element.textContent = text;
  // Syntax Highlight
  Prism.highlightElement(result_element);
  emitCodeChange(text);
}

function sync_scroll(element) {
  /* Scroll result to scroll coords of event - sync with textarea */
  let result_element = document.querySelector("#highlighting");
  // Get and set x and y
  result_element.scrollTop = element.scrollTop;
  result_element.scrollLeft = element.scrollLeft;
}

function check_tab(element, event) {
  let code = element.value;
  if (event.key == "Tab") {
    /* Tab key pressed */
    event.preventDefault(); // stop normal
    let before_tab = code.slice(0, element.selectionStart); // text before tab
    let after_tab = code.slice(element.selectionEnd, element.value.length); // text after tab
    let cursor_pos = element.selectionEnd + 1; // where cursor moves after tab - moving forward by 1 char to after tab
    element.value = before_tab + "\t" + after_tab; // add tab char
    // move cursor
    element.selectionStart = cursor_pos;
    element.selectionEnd = cursor_pos;
    update(element.value); // Update text to include indent
  }
}
/*This function emits the 'code_change' event to the server, sending the current text in the textarea as data.*/
function emitCodeChange(text) {
  const socketIoUrl = window.location.protocol + '//' + window.location.hostname + (window.location.port ? ':' + window.location.port : '');
  const socket = io.connect(socketIoUrl);
  socket.emit('code_change', { code: text });
}

function copyCode() {
  // Get the textarea element
  var copyText = document.getElementById("editing");

  // Select the text
  copyText.select();
  copyText.setSelectionRange(0, 99999); // For mobile devices

  // Copy the text to the clipboard
  document.execCommand("copy");

  // (Optional) Alert the copied text
  alert("Copied the code: " + copyText.value);
}

