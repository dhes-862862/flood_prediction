from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, db
import os

app = Flask(__name__)

# Firebase Admin Initialization
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://my-water-flow-project-default-rtdb.firebaseio.com/'
})

# Home route
@app.route('/')
def index():
    ref = db.reference('/')
    data = ref.get()

    # Extract necessary fields with fallback values
    flow_rate = data.get("flow_rate", "N/A")
    buzzer = data.get("buzzer", "N/A")
    led = data.get("led", "N/A")
    prediction = data.get("prediction", "N/A")

    # Notes based on prediction
    if prediction == "Yes":
        notes = "Avoid visiting Coutrallam – High Flood Risk"
    elif prediction == "Unpredictable":
        notes = "Caution Tourists at Coutrallam"
    else:
        notes = "No caution"

    return render_template("index.html",
                           flow_rate=flow_rate,
                           buzzer=buzzer,
                           led=led,
                           prediction=prediction,
                           notes=notes)

if __name__ == "__main__":
    app.run(debug=True)
