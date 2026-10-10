
import os
import time
import threading
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

API_TOKEN = os.environ.get("CCS_API_TOKEN")
lock = threading.Lock()
latest_reading = None

@app.get("/")
def health():
    return jsonify({"service": "ColdChain Sentinel receiver",
                    "status": "online"})

@app.post("/reading")
def receive_reading():
    global latest_reading

    if not API_TOKEN:
        abort(503, "Receiver token is not configured")

    token = request.headers.get("X-CCS-Token", "")
    if token != API_TOKEN:
        abort(401, "Unauthorized")

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, "Expected JSON")

    try:
        temp = float(data["temperature_c"])
        seq = int(data["seq"])
        device_id = str(data["device_id"])
    except (KeyError, TypeError, ValueError):
        abort(400, "Invalid reading fields")

    if not -55 <= temp <= 125 or seq < 0 or not device_id:
        abort(400, "Reading out of range")

    with lock:
        if latest_reading and latest_reading["device_id"] == device_id:
            if seq <= latest_reading["seq"]:
                return jsonify({
                    "error": "Stale or replayed sequence",
                    "received_seq": seq,
                    "last_accepted_seq": latest_reading["seq"],
                    "device_id": device_id
                }), 409

        latest_reading = {
            "device_id": device_id,
            "temperature_c": temp,
            "seq": seq,
            "received_at": time.time()
        }

    return jsonify({"accepted": True, "seq": seq})

@app.get("/latest")
def get_latest():
    if not API_TOKEN:
        abort(503, "Receiver token is not configured")

    token = request.headers.get("X-CCS-Token", "")
    if token != API_TOKEN:
        abort(401, "Unauthorized")

    with lock:
        if latest_reading is None:
            return jsonify({"status": "no_readings"}), 404
        return jsonify(latest_reading)

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=int(os.environ.get("PORT", "10000")))

