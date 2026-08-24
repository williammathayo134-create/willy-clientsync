import os
from flask import Flask, jsonify, request

app = Flask(__name__)
app.secret_key = 'willy_super_secret_key'

PRODUCTS = {}
TRANSACTIONS = []

@app.route('/')
def home():
    return "<h1>WILLY CLIENTSYNC SYSTEM</h1><p>API Server is live!</p>"

if __name__ == '__main__':
    app.run(debug=True)
