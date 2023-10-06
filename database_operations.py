import psycopg2
from tkinter import messagebox, filedialog
import tkinter as tk

DATABASE_CONFIG = {
    "dbname": "songdata",
    "user": "postgres",
    "password": "gal89478947",
    "host": "localhost",  # Change if your DB is not on localhost
    "port": "5432"
}

def get_connection():
    return psycopg2.connect(**DATABASE_CONFIG)

def get_db_details():
    conn = get_connection()
    # Assuming psycopg2 or similar library, extract connection details
    host = conn.get_dsn_parameters()['host']
    dbname = conn.get_dsn_parameters()['dbname']
    user = conn.get_dsn_parameters()['user']
    port = conn.get_dsn_parameters()['port']
    
    details = f"Connected to database '{dbname}' on host '{host}:{port}' as user '{user}'"
    conn.close()
    return details

def upload_song():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not filepath:
        return

    with open(filepath, "r") as f:
        lines = f.readlines()
        song_name = filepath.split("/")[-1].replace(".txt", "")
        writer_name = lines[0].strip()
        composer_name = lines[1].strip()
        year = int(lines[2].strip())
        lyrics = lines[3:]

    conn = get_connection()
    cur = conn.cursor()

    # Check if the writer already exists
    cur.execute("SELECT writer_id FROM SongWriters WHERE writer_name = %s;", (writer_name,))
    writer = cur.fetchone()
    if writer:
        writer_id = writer[0]
    else:
        # Insert writer
        cur.execute("INSERT INTO SongWriters (writer_name) VALUES (%s) RETURNING writer_id;", (writer_name,))
        writer_id = cur.fetchone()[0]

    # Check if the song already exists with the same name and writer
    cur.execute("SELECT song_id FROM Songs WHERE song_name = %s AND writer_id = %s;", (song_name, writer_id))
    existing_song = cur.fetchone()

    if existing_song:
        # Display a message box to inform the user that the song already exists
        messagebox.showerror("Duplicate Song", "This song has already been uploaded with the same writer.")
        cur.close()
        conn.close()
        return

    # Insert composer
    cur.execute("INSERT INTO Composers (composer_name) VALUES (%s) RETURNING composer_id;", (composer_name,))
    composer_id = cur.fetchone()[0]

    # Insert song
    cur.execute("INSERT INTO Songs (song_name, release_year, writer_id, composer_id) VALUES (%s, %s, %s, %s) RETURNING song_id;", (song_name, year, writer_id, composer_id))
    song_id = cur.fetchone()[0]

    # Insert words
    for line_num, line in enumerate(lyrics, start=1):
        words = line.strip().split()
        for word_num, word in enumerate(words, start=1):
            cur.execute("INSERT INTO Words (song_id, line_num, word_num, word) VALUES (%s, %s, %s, %s)",
                        (song_id, line_num, word_num, word))

    conn.commit()
    cur.close()
    conn.close()

    # Display a message box to inform the user that the song has been successfully uploaded
    messagebox.showinfo("Upload Successful", "The song has been successfully uploaded.")

def fetch_songs(song_listbox):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT song_name FROM Songs;")
        songs = cur.fetchall()
        for song in songs:
            song_listbox.insert(tk.END, song[0])
        cur.close()
        conn.close()