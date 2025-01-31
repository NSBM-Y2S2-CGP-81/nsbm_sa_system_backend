from flask import jsonify

def custom_function(data):
    if not data.get("input"):
        return jsonify({"error": "No input provided"}), 400

    result = data["input"].upper()  # Example transformation
    return jsonify({"result": result}), 200
