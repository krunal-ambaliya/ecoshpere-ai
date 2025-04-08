import eel
import sqlite3

# Initialize Eel with the folder containing web files
# eel.init('web')

# Connect to SQLite database
conn = sqlite3.connect('EchoSphear.db', check_same_thread=False)
cursor = conn.cursor()

# Create the table if it does not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sys_command (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        path TEXT NOT NULL
    )
''')
conn.commit()

# Function to add a command to the database
@eel.expose
def add_command(name, path):
    try:
        cursor.execute("INSERT INTO sys_command (name, path) VALUES (?, ?)", (name, path))
        conn.commit()
        return "Command added successfully!"
    except Exception as e:
        return f"Error: {e}"

# Function to fetch all commands
@eel.expose
def get_commands():
    cursor.execute("SELECT * FROM sys_command")
    return cursor.fetchall()

# Function to delete a command
@eel.expose
def delete_command(cmd_id):
    try:
        cursor.execute("DELETE FROM sys_command WHERE id = ?", (cmd_id,))
        conn.commit()
        return "Command deleted successfully!"
    except Exception as e:
        return f"Error: {e}"

# Start the Eel app
eel.start('ex.html', size=(800, 600))
