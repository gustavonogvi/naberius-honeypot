from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "honeypot.db")

@app.route("/events")
def get_events():
    ip    = request.args.get("ip")
    start = request.args.get("start")
    end   = request.args.get("end")

    query  = "SELECT * FROM events WHERE 1=1"
    params = []

    if ip:
        query += " AND ip = ?"
        params.append(ip)
    if start:
        query += " AND timestamp >= ?"
        params.append(start)
    if end:
        query += " AND timestamp <= ?"
        params.append(end)

    query += " ORDER BY timestamp DESC"

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

if __name__ == "__main__":
    app.run(debug=True)