from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
import psycopg2
import os

DATABASE_CONFIG = {
    "dbname": "railway",
    "user": "postgres",
    "password": "Qv9ObinCokJ26U0tdUKV",
    "host": "containers-us-west-64.railway.app",
    "port": "5833"
}

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
socketio = SocketIO(app, cors_allowed_origins="*")

try:
    conn = psycopg2.connect(**DATABASE_CONFIG)
except psycopg2.OperationalError as e:
    print(f"Could not connect to the database: {e}")


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


@app.route('/upload')
def upload():
    # Directory where problem files are stored
    problems_dir = 'problems'

    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()

        # Iterate through each file in the problems directory
        for filename in os.listdir('problems'):
            if filename.endswith(".txt"):
                problem_id = filename.rstrip('.txt')
                # Check if problem already exists in the database
                cur.execute(
                    "SELECT * FROM code_problems WHERE id = %s", (problem_id,))
                if cur.fetchone() is None:
                    # If not in database, read file and insert data
                    with open(os.path.join(problems_dir, filename)) as f:
                        content = f.read().split('\n')
                        problem_name = content[0]
                        difficulty = content[1]
                        exercise_description = content[2]
                        solution = "\n".join(content[4:])

                    cur.execute("""
                        INSERT INTO code_problems (id, problem_name, difficulty, exercise_description, solution) 
                        VALUES (%s, %s, %s, %s, %s)
                    """, (problem_id, problem_name, difficulty, exercise_description, solution))
                    conn.commit()
    except psycopg2.Error as e:
        print(f"Error interacting with database: {e}")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('index'))


@socketio.on('code_change')
def handle_code_change(json):
    # Broadcast the received code to all connected clients except the sender
    emit('update_code', json, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
