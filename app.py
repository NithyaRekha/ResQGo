from flask import Flask, render_template, request, jsonify, session
from logic import process_request, graph   # 🔥 IMPORTANT FIX

app = Flask(__name__)

# 🔐 SESSION SECRET KEY
app.secret_key = "resqgo_secret_key"

# 🏠 Home
@app.route('/')
def home():
    return render_template('home.html')

# 🚑 Request Page
@app.route('/request_page')
def request_page():
    return render_template('request.html', locations=list(graph.keys()))

# ℹ️ About
@app.route('/about')
def about():
    return render_template('about.html')

# 📞 Contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

# 📊 Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', data=session.get("latest_request"))

# 🚀 BACKEND API (FIXED)
@app.route('/request', methods=['POST'])
def request_ambulance():
    data = request.json
    result = process_request(data.get("location"))

    session['latest_request'] = {
        "patient": data.get("name"),
        "location": data.get("location"),
        "result": result
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)