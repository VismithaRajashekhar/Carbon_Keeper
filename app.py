import os
import json
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

generation_config = {"response_mime_type": "application/json"}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "You are an expert carbon footprint calculator. The user will provide a plain text description "
        "of an activity. Calculate the estimated CO2 emissions in kg. "
        "Return ONLY a JSON object with exactly these keys: "
        "'activity_summary' (brief string), 'co2_kg' (float), 'category' (string), "
        "'reduction_tip' (a specific, actionable tip to reduce this emission)."
    )
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/log', methods=['POST'])
def log_activity():
    data = request.json
    user_input = data.get('activity', '')

    if not user_input:
        return jsonify({"error": "No activity provided"}), 400

    try:
        response = model.generate_content(user_input)
        result = json.loads(response.text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
