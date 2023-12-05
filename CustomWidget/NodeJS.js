const express = require("express");
const https = require("https");
const fs = require("fs");
const bodyParser = require("body-parser");
const axios = require("axios");
const cors = require("cors");

// Configuration for HTTPS - replace with your certificate files
const options = {
    key: fs.readFileSync("path/to/YOUR.key"),
    cert: fs.readFileSync("path/to/YOUR.crt")
};

// Create Express app
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors());

// Port configuration
const port = process.env.PORT || 3000;

// Endpoint to handle requests
app.post("/score", function (req, res) {
    console.log("Request received:", req.body);

    // Call the Python Flask API
    callPythonAPI(req.body)
        .then(response => {
            console.log("Response from Python API:", response);
            res.status(200).send(response);
        })
        .catch(error => {
            console.error("Error calling Python API:", error);
            res.status(500).send("Error calling Python API");
        });
});

// Function to call Python Flask API
function callPythonAPI(data) {
    // Replace with your Flask API URL
    const flaskAPIURL = "http://localhost:5000/generate_commodity_response";
    
    return axios.post(flaskAPIURL, data)
        .then(response => response.data)
        .catch(error => {
            console.error("Error in callPythonAPI:", error);
            throw error;
        });
}

// Start HTTPS server
const server = https.createServer(options, app);
server.listen(port, () => {
    console.log(`Server running on https://localhost:${port}`);
});
