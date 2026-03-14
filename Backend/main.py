import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__, template_folder='.')

# It's recommended to set the API key as an environment variable
# For example: export OPENAI_API_KEY='your-key'
api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
client = OpenAI(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    