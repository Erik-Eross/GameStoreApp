import json
from google.cloud import storage
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main_route():
    bucket_name = "gamestore-bucket-s5623281"
    file_name = "featured_games.json"

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    data = blob.download_as_text()
    json_data = json.loads(data)

    return jsonify(json_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
