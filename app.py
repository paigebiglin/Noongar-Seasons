from flask import Flask, jsonify, send_from_directory
import csv

app = Flask(__name__, static_folder='static')

def load_seasons():
    with open('data/seasons.csv') as f:
        return list(csv.DictReader(f))

@app.route('/')
def home():
        return send_from_directory('static', 'index.html')

@app.route('/api/seasons')
def get_seasons():
        return jsonify(load_seasons())

if __name__ == '__main__':
        app.run(debug=True, port=5001)