from flask import Flask, render_template, request, jsonify
import json
import os
from supabase import create_client, Client

app = Flask(__name__)

# Supabase setup
url = "https://mgekkpwyguyvcfaoykkf.supabase.co"  # Replace with your Supabase URL
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nZWtrcHd5Z3V5dmNmYW95a2tmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAyNzM3NjgsImV4cCI6MjA2NTg0OTc2OH0.y-wXY83CdMjawtv89Ft0ZK0Hd_TOSquiLSuy1NMB8F0"  # Replace with your Supabase Anon Key
supabase: Client = create_client(url, key)

GAMEDAYS = [
    "2025-06-20", "2025-06-21", "2025-06-22",
    "2025-06-27", "2025-06-28", "2025-06-29",
    "2025-07-04", "2025-07-05", "2025-07-06",
    "2025-07-11", "2025-07-12", "2025-07-13",
    "2025-07-18", "2025-07-19", "2025-07-20",
    "2025-07-25", "2025-07-26", "2025-07-27"
]

TASKS = [
    "Referees", "Table team arrived", "Main Camera", "FT Cam", "3rd Camera", 
    "All Cameras Set", "Internet", "Walkies Charged", "Table Phone connected to display", 
    "Mic placed", "Commentators ready", "Game 1 logos set", "Game 1 Phone teams set",  
    "Game 1 Stream ready to go", "Game 1 sheets prepped", "Game 2 logos set", 
    "Game 2 Phone teams set", "Game 2 Stream ready to go", "Game 2 sheets prepped", 
    "Game 3 logos set", "Game 3 Phone teams set", "Game 3 sheets prepped", 
    "Game 3 Stream ready to go", "Interviews done", "Packup done"
]

# Initialize Supabase table for checklists
def init_db():
    for day in GAMEDAYS:
        # Check if the day exists in the Supabase table
        data = {
            "date": day,
            "items": json.dumps([False] * len(TASKS))  # Initial state: all unchecked
        }
        # Insert the data if it doesn't already exist
        supabase.table("checklists").upsert(data).execute()

@app.route("/")
def index():
    return render_template("index.html", gamedays=GAMEDAYS, tasks=TASKS)

@app.route("/get/<date>")
def get_checklist(date):
    response = supabase.table("checklists").select("items").eq("date", date).execute()
    if response.data:
        return jsonify(json.loads(response.data[0]["items"]))
    return jsonify([])

@app.route("/update/<date>", methods=["POST"])
def update_checklist(date):
    data = request.json.get("items", [])
    response = supabase.table("checklists").update({"items": json.dumps(data)}).eq("date", date).execute()
    return jsonify({"success": True})

import os

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT env var
    app.run(debug=True, host="0.0.0.0", port=port)
