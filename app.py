from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random
import time
import math

app = Flask(__name__)
CORS(app)

# ── HAVERSINE DISTANCE (km) ──
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# ── DRIVER DATA WITH GPS COORDINATES ──
# Each driver has a home base lat/lon (Bangalore area)
all_drivers = [
    # Gottigere / Bannerghatta area
    {"id":"D001","name":"Ravi Kumar",    "phone":"9876501111","vehicle":"KA-01-AA-1001","ambulance_type":"ICU Ambulance",          "lat":12.8729,"lon":77.5970,"area":"gottigere",       "available":True},
    {"id":"D002","name":"Suresh Babu",   "phone":"9876501112","vehicle":"KA-01-AA-1002","ambulance_type":"Basic Life Support",      "lat":12.8692,"lon":77.5958,"area":"gottigere",       "available":True},
    {"id":"D003","name":"Mohan Das",     "phone":"9876501113","vehicle":"KA-01-AA-1003","ambulance_type":"Advanced Life Support",   "lat":12.8750,"lon":77.5990,"area":"gottigere",       "available":True},
    # Vittasandra / Bellandur
    {"id":"D004","name":"Arjun Sharma",  "phone":"9876543210","vehicle":"KA-01-AB-1234","ambulance_type":"ICU Ambulance",          "lat":12.9259,"lon":77.6762,"area":"vittasandra",     "available":True},
    {"id":"D005","name":"Kiran Raj",     "phone":"9876543211","vehicle":"KA-01-AB-1235","ambulance_type":"Basic Life Support",      "lat":12.9230,"lon":77.6740,"area":"vittasandra",     "available":True},
    {"id":"D006","name":"Santosh P",     "phone":"9876543212","vehicle":"KA-01-AB-1236","ambulance_type":"Advanced Life Support",   "lat":12.9270,"lon":77.6780,"area":"vittasandra",     "available":True},
    # KR Market / City
    {"id":"D007","name":"Rahul Verma",   "phone":"9876502221","vehicle":"KA-01-KR-2001","ambulance_type":"ICU Ambulance",          "lat":12.9667,"lon":77.5788,"area":"kr market",       "available":True},
    {"id":"D008","name":"Anil Kumar",    "phone":"9876502222","vehicle":"KA-01-KR-2002","ambulance_type":"Basic Life Support",      "lat":12.9650,"lon":77.5800,"area":"kr market",       "available":True},
    {"id":"D009","name":"Deepak M",      "phone":"9876502223","vehicle":"KA-01-KR-2003","ambulance_type":"Advanced Life Support",   "lat":12.9680,"lon":77.5770,"area":"kr market",       "available":True},
    # Whitefield
    {"id":"D010","name":"Naveen G",      "phone":"9876503331","vehicle":"KA-01-WF-3001","ambulance_type":"ICU Ambulance",          "lat":12.9698,"lon":77.7499,"area":"whitefield",      "available":True},
    {"id":"D011","name":"Rajesh T",      "phone":"9876503332","vehicle":"KA-01-WF-3002","ambulance_type":"Basic Life Support",      "lat":12.9720,"lon":77.7510,"area":"whitefield",      "available":True},
    {"id":"D012","name":"Vinod S",       "phone":"9876503333","vehicle":"KA-01-WF-3003","ambulance_type":"Advanced Life Support",   "lat":12.9680,"lon":77.7480,"area":"whitefield",      "available":True},
    # Electronic City
    {"id":"D013","name":"Prakash N",     "phone":"9876504441","vehicle":"KA-01-EC-4001","ambulance_type":"ICU Ambulance",          "lat":12.8399,"lon":77.6770,"area":"electronic city", "available":True},
    {"id":"D014","name":"Ganesh R",      "phone":"9876504442","vehicle":"KA-01-EC-4002","ambulance_type":"Basic Life Support",      "lat":12.8420,"lon":77.6750,"area":"electronic city", "available":True},
    {"id":"D015","name":"Harish N",      "phone":"9876504443","vehicle":"KA-01-EC-4003","ambulance_type":"Advanced Life Support",   "lat":12.8380,"lon":77.6790,"area":"electronic city", "available":True},
    # Jayanagar
    {"id":"D016","name":"Darshan K",     "phone":"9876505551","vehicle":"KA-01-JY-5001","ambulance_type":"ICU Ambulance",          "lat":12.9252,"lon":77.5938,"area":"jayanagar",       "available":True},
    {"id":"D017","name":"Shiva Kumar",   "phone":"9876505552","vehicle":"KA-01-JY-5002","ambulance_type":"Basic Life Support",      "lat":12.9240,"lon":77.5920,"area":"jayanagar",       "available":True},
    {"id":"D018","name":"Manjunath B",   "phone":"9876505553","vehicle":"KA-01-JY-5003","ambulance_type":"Advanced Life Support",   "lat":12.9260,"lon":77.5950,"area":"jayanagar",       "available":True},
    # Koramangala
    {"id":"D019","name":"Vikram S",      "phone":"9876506661","vehicle":"KA-01-KM-6001","ambulance_type":"ICU Ambulance",          "lat":12.9352,"lon":77.6245,"area":"koramangala",     "available":True},
    {"id":"D020","name":"Lokesh B",      "phone":"9876506662","vehicle":"KA-01-KM-6002","ambulance_type":"Basic Life Support",      "lat":12.9340,"lon":77.6230,"area":"koramangala",     "available":True},
    {"id":"D021","name":"Anand K",       "phone":"9876506663","vehicle":"KA-01-KM-6003","ambulance_type":"Advanced Life Support",   "lat":12.9360,"lon":77.6260,"area":"koramangala",     "available":True},
    # HSR Layout
    {"id":"D022","name":"Sunil M",       "phone":"9876507771","vehicle":"KA-01-HS-7001","ambulance_type":"ICU Ambulance",          "lat":12.9081,"lon":77.6476,"area":"hsr layout",      "available":True},
    {"id":"D023","name":"Pradeep V",     "phone":"9876507772","vehicle":"KA-01-HS-7002","ambulance_type":"Basic Life Support",      "lat":12.9070,"lon":77.6460,"area":"hsr layout",      "available":True},
    {"id":"D024","name":"Nagaraj T",     "phone":"9876507773","vehicle":"KA-01-HS-7003","ambulance_type":"Advanced Life Support",   "lat":12.9090,"lon":77.6490,"area":"hsr layout",      "available":True},
    # Marathahalli
    {"id":"D025","name":"Rohit D",       "phone":"9876508881","vehicle":"KA-01-MH-8001","ambulance_type":"ICU Ambulance",          "lat":12.9591,"lon":77.6974,"area":"marathahalli",    "available":True},
    {"id":"D026","name":"Sanjay P",      "phone":"9876508882","vehicle":"KA-01-MH-8002","ambulance_type":"Basic Life Support",      "lat":12.9580,"lon":77.6960,"area":"marathahalli",    "available":True},
    {"id":"D027","name":"Raju G",        "phone":"9876508883","vehicle":"KA-01-MH-8003","ambulance_type":"Advanced Life Support",   "lat":12.9600,"lon":77.6990,"area":"marathahalli",    "available":True},
    # Indiranagar
    {"id":"D028","name":"Vivek Menon",   "phone":"9876509991","vehicle":"KA-01-IN-9001","ambulance_type":"ICU Ambulance",          "lat":12.9784,"lon":77.6408,"area":"indiranagar",     "available":True},
    {"id":"D029","name":"Krishnamurthy", "phone":"9876509992","vehicle":"KA-01-IN-9002","ambulance_type":"Basic Life Support",      "lat":12.9770,"lon":77.6390,"area":"indiranagar",     "available":True},
    # Hebbal
    {"id":"D030","name":"Prasad M",      "phone":"9876510001","vehicle":"KA-01-HB-0001","ambulance_type":"ICU Ambulance",          "lat":13.0350,"lon":77.5970,"area":"hebbal",          "available":True},
    {"id":"D031","name":"Ramesh K",      "phone":"9876510002","vehicle":"KA-01-HB-0002","ambulance_type":"Basic Life Support",      "lat":13.0360,"lon":77.5980,"area":"hebbal",          "available":True},
]

# ── HOSPITAL DATA WITH GPS ──
all_hospitals = [
    {"id":"H001","name":"Fortis Hospital Bannerghatta","rating":"4.6","phone":"08040502000","address":"Bannerghatta Road","lat":12.8733,"lon":77.5975,"specialties":["ICU","Cardiac","Trauma","Neuro"],"beds_available":12},
    {"id":"H002","name":"Apollo Hospitals Bannerghatta","rating":"4.5","phone":"08041334000","address":"Bannerghatta Road","lat":12.8980,"lon":77.5950,"specialties":["ICU","Cardiac","Ortho","Burn"],"beds_available":8},
    {"id":"H003","name":"Narayana Health City","rating":"4.8","phone":"08067506870","address":"Bommasandra","lat":12.8317,"lon":77.6825,"specialties":["ICU","Cardiac","Pediatric","Neuro","Trauma"],"beds_available":20},
    {"id":"H004","name":"Manipal Hospital Whitefield","rating":"4.6","phone":"18001024647","address":"Whitefield","lat":12.9698,"lon":77.7463,"specialties":["ICU","Ortho","Neuro","Cardiac"],"beds_available":15},
    {"id":"H005","name":"Sakra World Hospital","rating":"4.5","phone":"08049690000","address":"Marathahalli","lat":12.9564,"lon":77.6910,"specialties":["ICU","Cardiac","Trauma","Stroke"],"beds_available":10},
    {"id":"H006","name":"St. John's Medical College Hospital","rating":"4.3","phone":"08022065001","address":"Koramangala","lat":12.9346,"lon":77.6157,"specialties":["ICU","General","Ortho","Pediatric"],"beds_available":25},
    {"id":"H007","name":"Sagar Hospitals Jayanagar","rating":"4.3","phone":"08069555555","address":"Jayanagar","lat":12.9282,"lon":77.5834,"specialties":["ICU","Cardiac","Ortho","General"],"beds_available":14},
    {"id":"H008","name":"Manipal Hospitals Jayanagar","rating":"4.4","phone":"08022963500","address":"Jayanagar","lat":12.9299,"lon":77.5908,"specialties":["ICU","Neuro","Cardiac","Stroke"],"beds_available":9},
    {"id":"H009","name":"Victoria Hospital","rating":"3.3","phone":"08026701150","address":"Fort Road","lat":12.9613,"lon":77.5761,"specialties":["General","Trauma","Emergency"],"beds_available":30},
    {"id":"H010","name":"Bowring & Lady Curzon Hospital","rating":"3.5","phone":"08025320540","address":"Shivajinagar","lat":12.9810,"lon":77.6016,"specialties":["General","Emergency","Ortho"],"beds_available":18},
    {"id":"H011","name":"Sparsh Hospital","rating":"4.2","phone":"08039538000","address":"Infantry Road","lat":12.9895,"lon":77.6019,"specialties":["Trauma","Ortho","Spine","ICU"],"beds_available":11},
    {"id":"H012","name":"Aster CMI Hospital","rating":"4.5","phone":"08040891000","address":"Hebbal","lat":13.0375,"lon":77.5987,"specialties":["ICU","Cardiac","Neuro","Onco"],"beds_available":16},
    {"id":"H013","name":"Mazumdar Shaw Medical Center","rating":"4.6","phone":"08071222222","address":"Bommasandra","lat":12.8353,"lon":77.6814,"specialties":["Cardiac","Onco","ICU","Neuro"],"beds_available":7},
    {"id":"H014","name":"BGS Gleneagles Global Hospitals","rating":"4.4","phone":"08026730000","address":"Kengeri","lat":12.9050,"lon":77.5109,"specialties":["ICU","Transplant","Cardiac","Neuro"],"beds_available":13},
]

# ── EMERGENCY KEYWORD CLASSIFICATION ──
CRITICAL_KEYWORDS = [
    "heart attack","cardiac arrest","cardiac","myocardial","chest pain","chest tightness",
    "stroke","brain stroke","paralysis","unconscious","not breathing","not responding",
    "stopped breathing","accident","major accident","crash","head injury","trauma",
    "blood loss","heavy bleeding","internal bleeding","seizure","convulsion","overdose",
    "poisoning","electric shock","drowning","choking","anaphylaxis","allergic shock",
    "broken neck","spinal injury","burn","severe burn","stab wound","gunshot"
]
MODERATE_KEYWORDS = [
    "fever","high fever","vomiting","pain","stomach pain","abdominal pain","fall",
    "injury","dizziness","fainting","fainted","appendix","back pain","diabetic",
    "asthma","breathing difficulty","allergy","infection","wound","fracture",
    "broken bone","pregnancy","labor","delivery","blood pressure","hypertension",
    "kidney stone","urinary","migraine","eye injury","dog bite","snake bite"
]
LOW_KEYWORDS = [
    "cold","cough","flu","mild fever","headache","nausea","weakness","fatigue",
    "body ache","sore throat","rash","skin","insect bite","minor cut","bruise"
]

# Specialties needed per emergency type
EMERGENCY_SPECIALTIES = {
    "cardiac":    ["Cardiac","ICU"],
    "trauma":     ["Trauma","ICU"],
    "stroke":     ["Stroke","Neuro","ICU"],
    "neuro":      ["Neuro","ICU"],
    "ortho":      ["Ortho"],
    "pediatric":  ["Pediatric","ICU"],
    "burn":       ["Burn","ICU"],
    "general":    ["ICU","General"],
}

def classify_emergency_type(issue):
    t = issue.lower()
    if any(k in t for k in ["heart","cardiac","chest pain","myocardial"]):
        return "cardiac"
    if any(k in t for k in ["stroke","paralysis","brain"]):
        return "stroke"
    if any(k in t for k in ["accident","crash","trauma","head injury","stab","gunshot"]):
        return "trauma"
    if any(k in t for k in ["fracture","broken bone","ortho"]):
        return "ortho"
    if any(k in t for k in ["burn","fire"]):
        return "burn"
    if any(k in t for k in ["seizure","epilepsy","convulsion","neuro"]):
        return "neuro"
    if any(k in t for k in ["child","baby","infant","pediatric"]):
        return "pediatric"
    return "general"

def get_priority(issue):
    t = issue.lower()
    for kw in CRITICAL_KEYWORDS:
        if kw in t:
            return "critical", 5   # 5 seconds delay
    for kw in MODERATE_KEYWORDS:
        if kw in t:
            return "moderate", 22  # 22 seconds delay
    for kw in LOW_KEYWORDS:
        if kw in t:
            return "low", 50       # 50 seconds delay
    return "low", 50

def get_ambulance_type_needed(priority, emergency_type):
    if priority == "critical":
        return "ICU Ambulance"
    elif priority == "moderate":
        return "Advanced Life Support"
    else:
        return "Basic Life Support"

def find_nearest_driver(user_lat, user_lon, ambulance_type_needed, priority):
    """
    Smart driver selection:
    - For CRITICAL: must be ICU Ambulance, sorted by distance
    - For MODERATE: ALS preferred, or nearest available
    - For LOW: any available, sorted by distance
    """
    available = [d for d in all_drivers if d["available"]]

    # Score each driver
    scored = []
    for d in available:
        dist = haversine(user_lat, user_lon, d["lat"], d["lon"])
        # Type match bonus
        type_match = 1.0
        if priority == "critical":
            if d["ambulance_type"] == "ICU Ambulance":
                type_match = 0.0  # no penalty
            elif d["ambulance_type"] == "Advanced Life Support":
                type_match = 0.3  # small distance penalty
            else:
                type_match = 1.0  # large penalty for BLS in critical
        elif priority == "moderate":
            if d["ambulance_type"] in ["ICU Ambulance", "Advanced Life Support"]:
                type_match = 0.0
            else:
                type_match = 0.5
        # Score = distance + type penalty (in km equivalent)
        score = dist + (type_match * 5)
        scored.append({"driver": d, "dist_km": dist, "score": score})

    scored.sort(key=lambda x: x["score"])

    if not scored:
        return None, 0

    best = scored[0]
    return best["driver"], best["dist_km"]

def find_best_hospital(user_lat, user_lon, emergency_type, priority):
    """
    Smart hospital selection:
    - Match emergency specialty
    - Filter by bed availability
    - Sort by distance, weighted by rating
    """
    needed_specialties = EMERGENCY_SPECIALTIES.get(emergency_type, ["General","ICU"])

    scored = []
    for h in all_hospitals:
        if h["beds_available"] < 1:
            continue
        dist = haversine(user_lat, user_lon, h["lat"], h["lon"])
        # Specialty match score
        specialty_matches = sum(1 for s in needed_specialties if s in h["specialties"])
        specialty_score = specialty_matches / max(len(needed_specialties), 1)
        # Rating bonus (4-5 star hospitals preferred)
        rating = float(h["rating"])
        rating_bonus = (rating - 3.0) / 2.0  # 0.0 to 1.0

        # Score: lower is better
        # Distance heavily weighted, specialty & rating reduce distance penalty
        score = dist * (1.0 - 0.3 * specialty_score) * (1.0 - 0.1 * rating_bonus)

        scored.append({
            "hospital": h,
            "dist_km": round(dist, 2),
            "specialty_match": specialty_matches,
            "score": score
        })

    scored.sort(key=lambda x: x["score"])

    if not scored:
        return all_hospitals[0], 5.0

    best = scored[0]
    return best["hospital"], best["dist_km"]

def calculate_realistic_eta(dist_km, priority, time_of_day_hour=None):
    """
    ETA based on:
    - Distance
    - Priority (lights & siren reduce ETA for critical)
    - Bangalore traffic patterns
    """
    # Average speeds (km/h) considering Bangalore traffic
    if priority == "critical":
        avg_speed = 42  # With siren, can move faster
    elif priority == "moderate":
        avg_speed = 28
    else:
        avg_speed = 22

    # Traffic factor (rough Bangalore pattern)
    import datetime
    hour = datetime.datetime.now().hour
    if 8 <= hour <= 10 or 17 <= hour <= 20:  # Peak hours
        traffic_factor = 1.45
    elif 11 <= hour <= 16:  # Moderate
        traffic_factor = 1.15
    else:  # Off peak
        traffic_factor = 0.95

    if priority == "critical":
        traffic_factor = max(1.0, traffic_factor * 0.75)  # Siren cuts through traffic

    raw_minutes = (dist_km / avg_speed) * 60 * traffic_factor
    # Add dispatch + preparation time
    prep_time = 1.5 if priority == "critical" else 2.5

    eta = round(raw_minutes + prep_time)
    return max(2, min(eta, 45))  # Clamp between 2-45 min

def assign_emergency(location, name, phone, issue, lat=None, lon=None):
    priority, search_delay = get_priority(issue)
    emergency_type = classify_emergency_type(issue)
    ambulance_type_needed = get_ambulance_type_needed(priority, emergency_type)

    # Use GPS if available, otherwise use Bangalore center
    user_lat = lat if lat else 12.9716
    user_lon = lon if lon else 77.5946

    # Find nearest suitable driver
    driver, driver_dist = find_nearest_driver(user_lat, user_lon, ambulance_type_needed, priority)

    # Find best hospital
    hospital, hosp_dist = find_best_hospital(user_lat, user_lon, emergency_type, priority)

    # Calculate ETA
    eta = calculate_realistic_eta(driver_dist, priority)

    # Add driver coordinates to response for live tracking
    driver_with_pos = dict(driver)
    driver_with_pos["start_lat"] = driver["lat"] + (random.random() - 0.5) * 0.008
    driver_with_pos["start_lon"] = driver["lon"] + (random.random() - 0.5) * 0.008

    hospital_with_info = dict(hospital)
    hospital_with_info["dist_km"] = hosp_dist

    return {
        "driver":          driver_with_pos,
        "hospital":        hospital_with_info,
        "eta":             eta,
        "driver_dist_km":  round(driver_dist, 2),
        "status":          "En Route",
        "priority":        priority,
        "emergency_type":  emergency_type,
        "ambulance_needed": ambulance_type_needed,
        "search_delay":    search_delay
    }

# ── ROUTES ──
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/request')
def request_page():
    return render_template("request.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/history')
def history():
    return render_template("history.html")

@app.route('/request_ambulance', methods=['POST'])
def request_ambulance():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400

        name     = data.get("name", "")
        phone    = data.get("phone", "")
        issue    = data.get("issue", "")
        location = data.get("location", "")
        lat      = data.get("lat")
        lon      = data.get("lon")

        result = assign_emergency(location, name, phone, issue, lat, lon)

        return jsonify({
            "success":         True,
            "id":              int(time.time() * 1000),
            "name":            name,
            "phone":           phone,
            "issue":           issue,
            "location":        location,
            "lat":             lat,
            "lon":             lon,
            "driver":          result["driver"],
            "hospital":        result["hospital"],
            "eta":             result["eta"],
            "driver_dist_km":  result["driver_dist_km"],
            "status":          result["status"],
            "priority":        result["priority"],
            "emergency_type":  result["emergency_type"],
            "ambulance_needed":result["ambulance_needed"],
            "search_delay":    result["search_delay"]
        })

    except Exception as e:
        print("ERROR:", e)
        import traceback; traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/drivers/nearby', methods=['GET'])
def nearby_drivers():
    """API to get nearby available drivers for a given location"""
    lat = float(request.args.get('lat', 12.9716))
    lon = float(request.args.get('lon', 77.5946))
    limit = int(request.args.get('limit', 5))

    available = [d for d in all_drivers if d["available"]]
    with_dist = sorted(
        [{"driver": d, "dist_km": round(haversine(lat, lon, d["lat"], d["lon"]), 2)} for d in available],
        key=lambda x: x["dist_km"]
    )
    return jsonify(with_dist[:limit])

@app.route('/api/hospitals/nearby', methods=['GET'])
def nearby_hospitals():
    """API to get nearby hospitals"""
    lat  = float(request.args.get('lat', 12.9716))
    lon  = float(request.args.get('lon', 77.5946))
    limit = int(request.args.get('limit', 5))

    with_dist = sorted(
        [{"hospital": h, "dist_km": round(haversine(lat, lon, h["lat"], h["lon"]), 2)} for h in all_hospitals],
        key=lambda x: x["dist_km"]
    )
    return jsonify(with_dist[:limit])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
