import re
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return jsonify({"message": "Classifier Service is running successfully!"})

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    text = data["text"]
    detected_entities = []

    # Patterns
    patterns = {
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "Email": r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
        "Phone": r"\b(\+?\d{1,2}[ -]?)?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{4}\b",
        "Credit Card": r"\b(?:\d[ -]*?){13,16}\b",
        "IP Address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "URL": r"\bhttps?:\/\/[^\s]+",
        "Postal Code": r"\b\d{5}(?:-\d{4})?\b",
        "Date": r"\b(?:\d{1,2}[\/\.-]){2}\d{2,4}\b"
    }

    for entity, pattern in patterns.items():
        if re.search(pattern, text):
            detected_entities.append(entity)

    return jsonify({
        "received_text": text,
        "detected_entities": detected_entities,
        "status": "classified"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)