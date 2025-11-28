from flask import Flask, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    # Get MongoDB connection URI from environment variable
    mongo_uri = os.environ["MONGO_URI"]
    client = MongoClient(mongo_uri)

    db = client["gamestore"]
    reviews = db["reviews"]

    # Fetch latest 5 reviews
    latest_reviews = list(
        reviews.find().sort("timestamp", -1).limit(5)
    )

    # Convert ObjectId + datetime for JSON response
    for r in latest_reviews:
        r["_id"] = str(r["_id"])
        r["timestamp"] = str(r["timestamp"])

    return jsonify({"top_reviews": latest_reviews})

# Required for Cloud Run local execution
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
