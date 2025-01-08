from flask import Flask, render_template, jsonify, make_response, send_from_directory, request
import os
import random
import json

app = Flask(__name__)

FILENAME = "data/dostuff.events.json"
FILENAME_DET = "data/dostuff.detections.json"


# Static (reused by RedEdr.exe)

@app.route('/')
def index():
    return render_template('mock_index.html')

@app.route('/recordings')
def recordings():
    return render_template('mock_recording.html')

@app.route('/static/<path>')
def send_static(path):
    return send_from_directory('templates', path)


# API (to be implemented by RedEdr.exe)

@app.route('/api/events', methods=['GET', 'POST'])
def api_events():
    with open(FILENAME) as f:
        data = json.load(f)
    json_data = json.dumps(data, indent=4)
    response = make_response(json_data)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/detections', methods=['GET', 'POST'])
def api_detections():
    with open(FILENAME_DET) as f:
        data = json.load(f)
    json_data = json.dumps(data, indent=4)
    response = make_response(json_data)
    response.headers['Content-Type'] = 'application/json'
    response = make_response(jsonify(data))
    return response


@app.route('/api/stats')
def api_stats():
    data = {
        "events_count": 1,
        "detections_count": 42,
    }
    response = make_response(jsonify(data))
    return response


@app.route('/api/reset')
def api_reset():
    data = {
        "result": "ok",
    }
    response = make_response(jsonify(data))
    return response


@app.route('/api/save')
def api_save():
    data = {
        "result": "ok",
    }
    response = make_response(jsonify(data))
    return response


@app.route('/api/trace', methods=['GET', 'POST'])
def api_trace():

    if request.method == 'GET':
        return jsonify({"trace": "notepad.exe"})
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        traceName = data.get("trace", "")
        print("Tracing now: " + traceName)
        data = {
            "result": "ok",
        }
        response = make_response(jsonify(data))
        return response


def getRecordingsNames(directory):
    try:
        return [f[:f.index(".")] for f in os.listdir(directory) if f.endswith('.events.json')]
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
        return []
    except PermissionError:
        print(f"Permission denied to access '{directory}'.")
        return []


@app.route('/api/recordings')
def api_recordings():
    recordings = getRecordingsNames("data")
    response = make_response(jsonify(recordings))
    return response


@app.route('/api/recordings/<recordingname>')
def api_recording(recordingname):
    with open(f"data/{recordingname}.events.json") as f:
        data = json.load(f)
    json_data = json.dumps(data, indent=4)
    response = make_response(json_data)
    return response


if __name__ == '__main__':
    app.run(debug=True)

