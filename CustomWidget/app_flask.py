!pip install Flask

from flask import Flask, request, jsonify
import your_python_script  # Import your script here

app = Flask(__name__)

@app.route('/generate_commodity_response', methods=['POST'])
def generate_commodity_response():
    data = request.json
    start_date = data['start_date']
    end_date = data['end_date']
    commodity = data['commodity']
    prompt = data['prompt']
    
    response = your_python_script.generate_commodity_response(start_date, end_date, commodity, prompt)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)