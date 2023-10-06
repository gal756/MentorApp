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

@socketio.on('shared_code')
def handle_shared_code(json):
    # Broadcast the received code to all connected clients
    emit('shared_code', json, broadcast=True)

if __name__ == '__main__':
    socketio.run(app,debug=True,allow_unsafe_werkzeug=True, port=5912)
