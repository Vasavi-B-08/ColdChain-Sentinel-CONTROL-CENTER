
import os
import time
import threading
import math
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

API_TOKEN = os.environ.get("CCS_API_TOKEN")
lock = threading.Lock()

latest_reading = None
last_sequences = {}


@app.get("/")
def health():
    return jsonify({
        "service": "ColdChain Sentinel receiver",
        "status": "online"
    })


@app.post("/reading")
def receive_reading():
    global latest_reading

    if not API_TOKEN:
        abort(503, "Receiver token is not configured")

    if request.headers.get("X-CCS-Token", "") != API_TOKEN:
        abort(401, "Unauthorized")

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        abort(400, "Expected JSON")

    try:
        temp = float(data["temperature_c"])
        seq = int(data["seq"])
        device_id = str(data["device_id"]).strip()
        session_id = str(data["session_id"]).strip()
    except (KeyError, TypeError, ValueError):
        abort(400, "Invalid reading fields")

    if not math.isfinite(temp) or not (-55 <= temp <= 125) or seq < 0:
        abort(400, "Reading out of range")

    if not device_id or not session_id:
        abort(400, "Missing device_id or session_id")

    # New fields are optional so older sender code still works.
    humidity = None
    door_open = None

    if "humidity_pct" in data:
        try:
            humidity = float(data["humidity_pct"])
        except (TypeError, ValueError):
            abort(400, "Invalid humidity_pct")

        if not math.isfinite(humidity) or not (0 <= humidity <= 100):
            abort(400, "Humidity out of range")

    if "door_open" in data:
        if not isinstance(data["door_open"], bool):
            abort(400, "door_open must be true or false")
        door_open = data["door_open"]

    session_key = (device_id, session_id)

    with lock:
        previous_seq = last_sequences.get(session_key)

        if previous_seq is not None and seq <= previous_seq:
            return jsonify({
                "error": "Stale or replayed sequence",
                "received_seq": seq,
                "last_accepted_seq": previous_seq,
                "device_id": device_id,
                "session_id": session_id
            }), 409

        last_sequences[session_key] = seq

        latest_reading = {
            "device_id": device_id,
            "session_id": session_id,
            "temperature_c": temp,
            "humidity_pct": humidity,
            "door_open": door_open,
            "seq": seq,
            "received_at": time.time()
        }

    return jsonify({
        "accepted": True,
        "seq": seq,
        "session_id": session_id
    })


@app.get("/latest")
def get_latest():
    if not API_TOKEN:
        abort(503, "Receiver token is not configured")

    if request.headers.get("X-CCS-Token", "") != API_TOKEN:
        abort(401, "Unauthorized")

    with lock:
        if latest_reading is None:
            return jsonify({"status": "no_readings"}), 404

        return jsonify(latest_reading)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "10000"))
    )
