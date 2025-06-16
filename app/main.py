from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import datetime

app = Flask(__name__)

#Generate game days: all Fri, Sat, Sun from today till end of August


GAMEDAYS = [
    "2025-06-20", "2025-06-21", "2025-06-22",
    "2025-06-27", "2025-06-28", "2025-06-29",
    "2025-07-04", "2025-07-05", "2025-07-06",
    "2025-07-11", "2025-07-12", "2025-07-13",
    "2025-07-18", "2025-07-19", "2025-07-20",
    "2025-07-25", "2025-07-26", "2025-07-27"
]

TASKS = ["Referees", "Table team arrived", "Main Camera", "FT Cam", "3rd Camera", "All Cameras Set", "Internet ", "Walkies Charged", "Table Phone connected to display", "Mic placed", "Commentators ready", "Game 1 logos set", "Game 1 Phone teams set",  "Game 1 Stream ready to go", "Game 1 sheets prepped", "Game 2 logos set", "Game 2 Phone teams set", "Game 2 Stream ready to go", "Game 2 sheets prepped", "Game 3 logos set", "Game 3 Phone teams set", "Game 3 sheets prepped",  "Game 3 Stream ready to go", "Interviews done", "Packup done"]

# Initialize DB
def init_db():
    conn = sqlite3.connect("checklist.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS checklist (date TEXT PRIMARY KEY, items TEXT)")
    for day in GAMEDAYS:
        c.execute("INSERT OR IGNORE INTO checklist (date, items) VALUES (?, ?)",
                  (day, json.dumps([False] * len(TASKS))))
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html", gamedays=GAMEDAYS, tasks=TASKS)

@app.route("/get/<date>")
def get_checklist(date):
    conn = sqlite3.connect("checklist.db")
    c = conn.cursor()
    c.execute("SELECT items FROM checklist WHERE date = ?", (date,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify(json.loads(row[0]))
    return jsonify([])

@app.route("/update/<date>", methods=["POST"])
def update_checklist(date):
    data = request.json.get("items", [])
    conn = sqlite3.connect("checklist.db")
    conn.execute("UPDATE checklist SET items = ? WHERE date = ?", (json.dumps(data), date))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

import os

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT env var
    app.run(debug=True, host="0.0.0.0", port=port)

