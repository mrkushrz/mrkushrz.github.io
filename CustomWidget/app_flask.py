from flask import Flask, request, jsonify
import os
import Backend  # Import your Backend script

app = Flask(__name__)

@app.route('/generate_commodity_response', methods=['POST'])
def generate_commodity_response():
    try:
        # Extract data from request
        data = request.json
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        commodity = data.get('commodity')
        prompt = data.get('prompt')

        # Check for missing data
        if not all([start_date, end_date, commodity, prompt]):
            return jsonify({"error": "Missing data in request"}), 400

        # Call the function from Backend.py
        response = Backend.generate_commodity_response(start_date, end_date, commodity, prompt)
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use environment variable for port or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
