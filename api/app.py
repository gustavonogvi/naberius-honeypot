from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "naberius.db")

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

@app.route("/stats/brute-force")
def brute_force():
    threshold = int(request.args.get("threshold", 5))
    window    = int(request.args.get("window", 60))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ip, COUNT(*) as attempts, MAX(timestamp) as last_seen,
               MAX(country) as country, MAX(city) as city
        FROM events
        WHERE timestamp >= datetime('now', ? || ' minutes')
        GROUP BY ip
        HAVING attempts >= ?
        ORDER BY attempts DESC
    """, (f"-{window}", threshold))
    rows = [{"ip": r[0], "attempts": r[1], "last_seen": r[2],
             "country": r[3], "city": r[4]} for r in cursor.fetchall()]
    conn.close()
    return jsonify(rows)


@app.route("/stats/top-credentials")
def top_credentials():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, COUNT(*) as count
        FROM events
        WHERE username IS NOT NULL
        GROUP BY username
        ORDER BY count DESC
        LIMIT 10
    """)
    usernames = [{"value": row[0], "count": row[1]} for row in cursor.fetchall()]

    cursor.execute("""
        SELECT password, COUNT(*) as count
        FROM events
        WHERE password IS NOT NULL
        GROUP BY password
        ORDER BY count DESC
        LIMIT 10
    """)
    passwords = [{"value": row[0], "count": row[1]} for row in cursor.fetchall()]

    conn.close()
    return jsonify({"usernames": usernames, "passwords": passwords})


if __name__ == "__main__":
    app.run(debug=True)