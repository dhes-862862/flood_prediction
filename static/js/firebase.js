// Import the necessary Firebase functions
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.1/firebase-app.js";
import { getDatabase, ref, onValue } from "https://www.gstatic.com/firebasejs/9.22.1/firebase-database.js";

// Firebase configuration (replace with your credentials)
const firebaseConfig = {
  apiKey: "AIzaSyCt1SuZh-dSKGX-FoFMvDGAJDSNUkvaZ4Q",
  authDomain: "my-water-flow-project.firebaseapp.com",
  databaseURL: "https://my-water-flow-project-default-rtdb.firebaseio.com",
  projectId: "my-water-flow-project",
  storageBucket: "my-water-flow-project.firebasestorage.app",
  messagingSenderId: "669975750113",
  appId: "1:669975750113:web:13dc07197139fc2a349ea0",
  measurementId: "G-RM1WG8H61G"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

// Reference to the Realtime Database (root)
const dbRef = ref(db, '/');

// Listen for real-time updates
onValue(dbRef, (snapshot) => {
  const data = snapshot.val();
  console.log("Data from Firebase:", data);  // Log the entire data object

  // Check if data is available
  if (data) {
    // Access fields from the data
    const buzzerState = data.buzzerState || "N/A";
    const flowRate = data.flowRate || "N/A";
    const greenLEDState = data.greenLEDState || "N/A";
    
    // Prediction data might not exist in all cases, handle that gracefully
    const predictionData = data.predictionData || {};
    const waterfallName = predictionData.waterfallName || "N/A";
    const districtName = predictionData.districtName || "N/A";
    const floodRisk = predictionData.floodRisk || "N/A";
    const rainfallRate = predictionData.rainfallRate || "N/A";
    const temperature = predictionData.temperature || "N/A";
    const time = predictionData.time || "N/A";

    // Update the HTML elements if they exist
    const updateElement = (id, value) => {
      const element = document.getElementById(id);
      if (element) {
        element.innerText = value;
      } else {
        console.warn(`Element with id "${id}" not found.`);
      }
    };

    // Display the data on the webpage
    updateElement("buzzerState", `Buzzer State: ${buzzerState}`);
    updateElement("flowRate", `Flow Rate: ${flowRate} mL/s`);
    updateElement("greenLEDState", `Green LED State: ${greenLEDState}`);
    updateElement("waterfallName", `Waterfall Name: ${waterfallName}`);
    updateElement("districtName", `District: ${districtName}`);
    updateElement("floodRisk", `Flood Risk: ${floodRisk}`);
    updateElement("rainfallRate", `Rainfall Rate: ${rainfallRate}`);
    updateElement("temperature", `Temperature: ${temperature}`);
    updateElement("time", `Time: ${time}`);
  } else {
    console.error("No data found in Firebase.");
  }
});
