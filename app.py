from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import datetime
import jwt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'willy_super_secret_key_2026'

users_db = {}

@app.route('/')
def home():
    return jsonify({"message": "Willy ClientSync Backend Running with Encryption!"})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Tafadhali weka username na password"}), 400

    if username in users_db:
        return jsonify({"error": "Mtumiaji huyu tayari yupo"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users_db[username] = hashed_password

    return jsonify({"message": f"Mtumiaji {username} amesajiliwa kwa usalama!"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user_password_hash = users_db.get(username)

    if user_password_hash and bcrypt.check_password_hash(user_password_hash, password):
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({"message": "Umeingia kikamilifu!", "token": token}), 200

    return jsonify({"error": "Username au Password sio sahihi"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
