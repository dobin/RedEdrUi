from flask import Flask, render_template, jsonify, make_response

import random
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/events', methods=['GET', 'POST'])
def api_events():
    # Load JSON data from file
    with open('data/notepad.json') as f:
        data = json.load(f)
    
    json_data = json.dumps(data, indent=4)  # Convert to JSON string with indentation for readability
    response = make_response(json_data)
    response.headers['Content-Type'] = 'application/json'
    
    return response

@app.route('/api/detections', methods=['GET', 'POST'])
def api_detections():
    # Sample JSON data
    data = [
        "aaaa",
        "bbbb",
    ]
    response = make_response(jsonify(data))
    return response


@app.route('/api/stats', methods=['GET', 'POST'])
def api_stats():
    #data = {
    #    "events": random.randint(1, 100),
    #    "users": random.randint(1, 100),
    #}
    #response = make_response(jsonify(data))
    data = "Stat1: 1234 <br>  Stat2: 4444"
    response = make_response(data)
    return response


@app.route('/api/reset', methods=['GET', 'POST'])
def api_reset():
    #data = {
    #    "events": random.randint(1, 100),
    #    "users": random.randint(1, 100),
    #}
    #response = make_response(jsonify(data))
    data = "ok"
    response = make_response(data)
    return response


if __name__ == '__main__':
    app.run(debug=True)

