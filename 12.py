from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print("Message received: " + message)
    socketio.emit('message', {'message': message}, room=request.sid, include_self=False)

@socketio.on('shared_code')
def handle_shared_code(shared_code):
    socketio.emit('shared_code', {'sharedCode': shared_code}, include_self=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
