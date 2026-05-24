from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from logic import process_request
import math

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

# ---------------- DRIVERS ----------------
drivers = {
    "KA-01-AB-1234": {"name": "Ravi Kumar", "lat": 12.97, "lon": 77.59, "available": True},
    "KA-02-CD-5678": {"name": "Suresh", "lat": 12.96, "lon": 77.61, "available": True},
    "KA-03-EF-9999": {"name": "Arjun", "lat": 12.95, "lon": 77.58, "available": True}
}

requests_db = {}

# ---------------- DISTANCE ----------------
def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/request', methods=['GET'])
def request_page():
    return render_template('request.html')

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# ---------------- REQUEST AMBULANCE ----------------
@app.route('/request', methods=['POST'])
def request_ambulance():

    data = request.get_json()

    print(data)

    user_lat = float(data["lat"])
    user_lon = float(data["lon"])

    nearest = None
    min_dist = float("inf")

    for d_id, d in drivers.items():
        if d["available"]:
            dist = distance(user_lat, user_lon, d["lat"], d["lon"])

            if dist < min_dist:
                min_dist = dist
                nearest = d_id

    if not nearest:
        return jsonify({"error": "No ambulances available"})

    driver = drivers[nearest]
    driver["available"] = False

    request_id = "REQ_" + nearest

    requests_db[request_id] = {
        "driver_id": nearest,
        "user_lat": user_lat,
        "user_lon": user_lon,
        "status": "assigned"
    }

    return jsonify({
        "request_id": request_id,
        "name": data["name"],
        "phone": data["phone"],
        "email": data["email"],
        "location": data["location"],
        "hospital": "Apollo Hospital",
        "ambulance": nearest,
        "driver_name": driver["name"],
        "eta": "10 mins"
    })

# ---------------- SOCKET LIVE TRACKING ----------------
@socketio.on("driver_location")
def driver_location(data):

    driver_id = data["driver_id"]

    if driver_id in drivers:
        drivers[driver_id]["lat"] = data["lat"]
        drivers[driver_id]["lon"] = data["lon"]

    socketio.emit("live_update", data)

# ---------------- RUN ----------------
if __name__ == "__main__":
    socketio.run(app, debug=True, port=5001, allow_unsafe_werkzeug=True)