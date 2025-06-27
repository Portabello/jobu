from flask import Flask, request, jsonify
from openai_service import get_gpt_response

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"response": "Please send a message."})

    reply = get_gpt_response(user_message)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
