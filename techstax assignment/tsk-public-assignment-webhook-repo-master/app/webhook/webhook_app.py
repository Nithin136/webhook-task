# webhook_app.py
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient("mongodb+srv://21891a7253nithin:8vyQcPoOgveg217V@cluster0.0luyika.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.get_database("webhooks")
collection = db.get_collection("events")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    print("Webhook received")
    data = request.json
    event_type = request.headers.get("X-GitHub-Event")
    print("Event Type:", event_type)

    if event_type == "push":
        print("Handling push event")
        author = data["pusher"]["name"]
        to_branch = data["ref"].split("/")[-1]
        timestamp = data["head_commit"]["timestamp"]

        collection.insert_one({
            "author": author,
            "event": "push",
            "to_branch": to_branch,
            "timestamp": timestamp
        })

    elif event_type == "pull_request":
        print("Handling pull_request event")
        action = data["action"]

        if action in ["opened", "closed"]:
            author = data["pull_request"]["user"]["login"]
            from_branch = data["pull_request"]["head"]["ref"]
            to_branch = data["pull_request"]["base"]["ref"]

            if action == "closed" and data["pull_request"].get("merged", False):
                event_name = "merge"
                timestamp = data["pull_request"]["merged_at"]
            else:
                event_name = "pull_request"
                timestamp = data["pull_request"]["created_at"]

            collection.insert_one({
                "author": author,
                "event": event_name,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            })

    return "Webhook received", 200

@app.route("/events")
def events():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    for event in events:
        event["_id"] = str(event["_id"])
    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)
