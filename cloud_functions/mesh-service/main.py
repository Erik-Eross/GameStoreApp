import requests
from flask import jsonify, Request

#endpoints
FEATURED_URL = "https://featured-games-104703165942.europe-west2.run.app"
REVIEWS_URL = "https://top-reviews-104703165942.europe-west2.run.app"

def main(request: Request):
    #featured games
    try:
        featured = requests.get(FEATURED_URL).json().get("featured", [])
    except:
        featured = []

    #top reviews
    try:
        reviews = requests.get(REVIEWS_URL).json().get("top_reviews", [])
    except:
        reviews = []

    return jsonify({
        "featured": featured,
        "top_reviews": reviews
    })
