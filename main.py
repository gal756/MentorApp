from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/choose_block')
def code_block():
    return render_template('choose_block.html')

@app.route('/edit_block')
def edit_code():
    return render_template('edit_block.html')

@socketio.on('message')
def handle_message(message):
    print("Message received: " + message)
    socketio.emit('message', {'message': message}, room=request.sid, include_self=False)

@socketio.on('shared_code')
def handle_shared_code(shared_code):
    socketio.emit('shared_code', {'sharedCode': shared_code}, include_self=True)

if __name__ == '__main__':
    socketio.run(app,debug=True, port=5000)
