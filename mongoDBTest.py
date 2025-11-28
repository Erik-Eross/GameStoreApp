from pymongo import MongoClient
import os

# Manually set your MONGO_URI here
mongo_uri = "mongodb+srv://s5623281_db_user:CqqS7OoC4wGIltG2@cluster0.3joitcy.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)
print("Mongo URI: ", os.environ.get(mongo_uri))

# Test connection
db = client["gamestore"]
reviews_collection = db["reviews"]

# Fetch the top 5 reviews
reviews = list(reviews_collection.find().sort("timestamp", -1).limit(5))

print(reviews)