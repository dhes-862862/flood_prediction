from flask import Flask, render_template_string
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")  # Firebase Admin SDK JSON file path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://my-water-flow-project-default-rtdb.firebaseio.com'
})

# HTML template with conditional alert heading
template = """
<!DOCTYPE html>
<html>
<head>
  <title>Realtime Flood Prediction</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f7f7f7;
      text-align: center;
    }
    .container {
      background: white;
      width: 80%;
      margin: 30px auto;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 0 15px rgba(0,0,0,0.1);
    }
    h1 {
      background-color: #ddd;
      padding: 15px;
    }
    .safe {
      color: green;
    }
    .danger {
      color: red;
    }
    .label {
      font-weight: bold;
    }
    .risk-low {
      color: green;
    }
    .risk-high {
      color: red;
    }
    .section-divider {
      margin-top: 30px;
      border-top: 1px solid #ccc;
      padding-top: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Realtime Data</h1>

    {% set show_warning = (prediction.Note == "Potential Risk and Caution Tourists at Coutrallam, due to present weather condition") or (prediction.PredictedFloodRisk == "Yes") %}
    
    {% if show_warning %}
      <h2 class="danger">Caution Tourists at Coutrallam</h2>
    {% else %}
      <h2 class="safe">Best Day for Vacation</h2>
    {% endif %}

    <p><span class="label">Predicted Date:</span> {{ prediction.PredictedDate or "N/A" }}</p>
   
    <p><span class="label">Falls Name:</span> {{ prediction.FallsName or "N/A" }}</p>
          <p><span class="label">Flood Risk:</span> <span class="{{ 'risk-high' if prediction.PredictedFloodRisk == 'Yes' else 'risk-low' }}">{{ prediction.PredictedFloodRisk or "Unknown" }}</span></p>

    <p><span class="label">Recommended Action:</span> {{ prediction.RecommendedAction or "N/A" }}</p>    
<p><span class="label">Date Time:</span> {{ prediction.Time or "N/A" }}</p>
    
    <p><span class="label">Today's Note:</span> {{ prediction.Note or "N/A" }}</p>
  

    <div class="section-divider">
      <h2>Sensor Data</h2>
      <p><span class="label">Flow Rate:</span> {{ flowRate or "N/A" }} mL/sec</p>
      <p><span class="label">Buzzer State:</span> {{ buzzer or "N/A" }}</p>
      <p><span class="label">Green LED:</span> {{ greenLED or "N/A" }}</p>
      <p><span class="label">Red LED:</span> {{ redLED or "N/A" }}</p>
    </div>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    root = db.reference("/")
    data = root.get()

    prediction = data.get("FloodPrediction", {})
    flowRate = data.get("flowRate", "N/A")
    buzzer = data.get("buzzerState", "N/A")
    greenLED = data.get("greenLEDState", "N/A")
    redLED = data.get("redLEDState", "N/A")

    return render_template_string(template, prediction=prediction,
                                  flowRate=flowRate, buzzer=buzzer,
                                  greenLED=greenLED, redLED=redLED)

if __name__ == "__main__":
    app.run(debug=True)
