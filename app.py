from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("clientsync.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    try:
        conn = sqlite3.connect("clientsync.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return jsonify({"message": "Usajili umekamilika kikamilifu"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Username tayari ipo"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    conn = sqlite3.connect("clientsync.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"message": "Imefanikiwa", "token": f"token_secret_{username}"}), 200
    return jsonify({"message": "Username au Password sio sahihi"}), 401

@app.route('/clients', methods=['GET'])
def get_clients():
    conn = sqlite3.connect("clientsync.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone FROM clients")
    rows = cursor.fetchall()
    conn.close()
    clients = [{"name": r[0], "phone": r[1]} for r in rows]
    return jsonify(clients), 200

@app.route('/clients', methods=['POST'])
def add_client():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    if not name or not phone:
        return jsonify({"message": "Jaza jina na namba ya simu"}), 400
    conn = sqlite3.connect("clientsync.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()
    return jsonify({"message": "Mteja ameongezwa kikamilifu!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
