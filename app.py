from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder='www', static_url_path='')
CORS(app)

DB = 'EchoSphear.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# Serve the frontend (index.html, CSS, JS)
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Fetch all commands
@app.route('/commands', methods=['GET'])
def get_commands():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, * FROM sys_command")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# Add new command
@app.route('/add-command', methods=['POST'])
def add_command():
    data = request.json
    name = data.get('name')
    path = data.get('path')
    if not name or not path:
        return jsonify({"error": "Missing data"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sys_command (name, path) VALUES (?, ?)", (name, path))
    conn.commit()
    conn.close()
    return jsonify({"message": "Command added"}), 201

# Delete a command
@app.route('/delete-command/<int:cmd_id>', methods=['DELETE'])
def delete_command(cmd_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sys_command WHERE rowid = ?", (cmd_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Command deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
