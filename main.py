from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
import psycopg2
from psycopg2 import pool
import os

# Database configuration using environment variables
DATABASE_CONFIG = {
    "dbname": os.environ.get("DB_NAME", "default_db_name"),
    "user": os.environ.get("DB_USER", "default_user"),
    "password": os.environ.get("DB_PASSWORD", "default_password"),
    "host": os.environ.get("DB_HOST", "default_host"),
    "port": os.environ.get("DB_PORT", "default_port")
}

# Flask application setup
app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
socketio = SocketIO(app, cors_allowed_origins="*")

# Attempt to connect to the PostgreSQL database
# try:
#     conn = psycopg2.connect(**DATABASE_CONFIG)
# except psycopg2.OperationalError as e:
#     # Print an error message if the connection fails
#     print(f"Could not connect to the database: {e}")

# Create a connection pool
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1, 20, **DATABASE_CONFIG)
    if connection_pool:
        print("Connection pool created successfully")
except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)


# Global variable to store the current problem being edited by a student
current_student_problem = None


# Define the route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for students to choose a code block
@app.route('/student_choose_block')
def student_block():
    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()
        # Query to get the last 4 problems ordered by id
        cur.execute("SELECT * FROM code_problems ORDER BY id DESC LIMIT 4")
        problems = cur.fetchall()
    except psycopg2.Error as e:
        # Print an error message if there is an issue with the database
        print(f"Error interacting with database: {e}")
        problems = []
    finally:
        # Close the database connection
        cur.close()
        connection_pool.putconn(conn)
    return render_template('student_choose_block.html', problems=problems)

# Route for mentors to choose a code block
@app.route('/mentor_choose_block')
def mentor_block():
    global current_student_problem
    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()
        # Query to get the last 4 problems ordered by id
        cur.execute("SELECT * FROM code_problems ORDER BY id DESC LIMIT 4")
        problems = cur.fetchall()

    except psycopg2.Error as e:
        # Print an error message if there is an issue with the database
        print(f"Error interacting with the database: {e}")
        problems = []
    finally:
        # Close the database connection
        cur.close()
        connection_pool.putconn(conn)
    return render_template('mentor_choose_block.html', problems=problems, current_student_problem=current_student_problem)

# Route for editing a specific code block
@app.route('/edit_block/<int:problem_id>')
def edit_block(problem_id):
    global current_student_problem  # Access the global variable
    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM code_problems WHERE id = %s", (problem_id,))
        problem = cur.fetchone()
    except psycopg2.Error as e:
        # Print an error message if there is an issue with the database
        print(f"Error interacting with the database: {e}")
        problem = None
    finally:
        # Update the global variable with the current problem being
                # edited by a student
        current_student_problem = problem_id
        cur.close()
        connection_pool.putconn(conn)

    if problem is None:
        # Handle the case where no problem is found
        return render_template('404.html'), 404

    return render_template('edit_block.html', problem=problem)


# Route for viewing a specific code block
@app.route('/view_block/<int:problem_id>')
def view_block(problem_id):
    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM code_problems WHERE id = %s", (problem_id,))
        problem = cur.fetchone()
    except psycopg2.Error as e:
        # Print an error message if there is an issue with the database
        print(f"Error interacting with the database: {e}")
        problem = None
    finally:
        cur.close()
        connection_pool.putconn(conn)

    if problem is None:
        # Handle the case where no problem is found
        return render_template('404.html'), 404

    return render_template('view_block.html', problem=problem)

# Route for uploading problems from files to the database
@app.route('/upload')
def upload():
    # Directory where problem files are stored
    problems_dir = 'problems'

    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()

        # Iterate through each file in the problems directory
        for filename in os.listdir(problems_dir):
            if filename.endswith(".txt"):
                problem_id = filename.rstrip('.txt')
                # Check if problem already exists in the database
                cur.execute("SELECT * FROM code_problems WHERE id = %s", (problem_id,))
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
        # Print an error message if there is an issue with the database
        print(f"Error interacting with database: {e}")
    finally:
        cur.close()
        connection_pool.putconn(conn)

    return redirect(url_for('index'))

# SocketIO event handler for handling code changes
@socketio.on('code_change')
def handle_code_change(json):
    # Broadcast the received code to all connected clients except the sender
    emit('update_code', json, broadcast=True, include_self=False)

# Run the Flask application with SocketIO support
if __name__ == '__main__':
    socketio.run(app, debug=True, port=port)
