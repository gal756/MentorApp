from flask import Flask, render_template
from flask_socketio import SocketIO,emit
import os

app = Flask(__name__)
port = int(os.environ.get("PORT", 5912))
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/choose_block')
def code_block():
    return render_template('choose_block.html')

@app.route('/edit_block')
def edit_code():
    return render_template('edit_block.html')

@app.route('/view_block')
def view_block():
    return render_template('view_block.html')

@socketio.on('code_change')
def handle_code_change(json):
    # Broadcast the received code to all connected clients except the sender
    emit('update_code', json, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app,debug=True,allow_unsafe_werkzeug=True, port=5912)
