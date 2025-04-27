from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "helixkitten_secret_key"  # Random secret for sessions

# Pre-set valid badge IDs and PINs
valid_credentials = {
    "12345": "4321",
    "67890": "9876"
}

# In-memory list to store access logs
access_logs = []

# Function to log badge/PIN attempts
def log_attempt(badge_id, pin_entered, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    log_entry = f"Timestamp: {timestamp} | Badge ID: {badge_id} | PIN Entered: {pin_entered} | Result: {result}"
    access_logs.append(log_entry)

# Step 1: Badge Scan Page
@app.route("/", methods=["GET", "POST"])
def badge_scan():
    error = None
    if request.method == "POST":
        badge_id = request.form.get("badge_id")
        if badge_id in valid_credentials:
            session["badge_id"] = badge_id
            return redirect(url_for("pin_entry"))
        else:
            error = "Access Denied: Invalid Badge."
            log_attempt(badge_id, "N/A", "Access Denied: Invalid Badge")
    return render_template("badge.html", error=error)

# Step 2: PIN Entry Page
@app.route("/pin", methods=["GET", "POST"])
def pin_entry():
    if "badge_id" not in session:
        return redirect(url_for("badge_scan"))

    badge_id = session["badge_id"]
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "pin":
            pin = request.form.get("pin")
            if valid_credentials[badge_id] == pin:
                log_attempt(badge_id, pin, "Access Granted")
                return redirect(url_for("success_page"))  # Success on correct PIN
            else:
                log_attempt(badge_id, pin, "Access Denied: Incorrect PIN")
                return redirect(url_for("denied_page"))  # Denied on wrong PIN
        
        elif action == "biometric":
            return redirect(url_for("fingerprint_scan"))
    
    return render_template("pin.html")

# Step 3: Simulated Fingerprint Scan Page
@app.route("/fingerprint")
def fingerprint_scan():
    badge_id = session.get("badge_id", "Unknown")
    log_attempt(badge_id, "Biometric", "Access Granted")
    return render_template("fingerprint_scan.html")

# Step 4: Access Granted Page
@app.route("/success")
def success_page():
    return render_template("success.html")

# Step 5: Access Denied Page
@app.route("/denied")
def denied_page():
    return render_template("denied.html")

# Step 6: View Access Logs Page (now reads from memory not file)
@app.route("/logs")
def view_logs():
    return render_template("access_logs.html", logs=access_logs)

# Step 7: Logout Route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('badge_scan'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
