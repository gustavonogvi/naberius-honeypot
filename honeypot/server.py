import socket
import datetime
import sqlite3
import os
import requests

HOST = "0.0.0.0"
PORT = 2222

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "honeypot.db")
GEO_API = "http://ip-api.com/json/"

def get_geo(ip):
    try:
        response = requests.get(f"{GEO_API}{ip}", timeout=5)
        data = response.json()
        if data.get("status") == "success":
            return {
                "country": data.get("country"),
                "city": data.get("city"),
                "region": data.get("regionName"),
                "asn": data.get("as"),
            }
    except Exception:
        pass
    return {"country": None, "city": None, "region": None, "asn": None}

#def func to log events 
def log_event(ip, port, payload):
    timestamp = datetime.datetime.now().isoformat()
    geo = get_geo(ip)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO events (ip, port, timestamp, payload, country, city, region, asn) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
        (ip, port, timestamp, payload, geo["country"], geo["city"], geo["region"], geo["asn"])
    )

    conn.commit()
    conn.close()

    print(f"[{timestamp}] {ip}:{port} | {geo['country']} {geo['city']} -> {payload!r}")


#now lets start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(13)
    print(f"Honeypot server started on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        conn.send(b"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6\r\n")
        ip = addr[0]
        payload = conn.recv(1024).decode(errors="ignore")
        log_event(ip, PORT, payload)
        conn.close()

if __name__ == "__main__":
    start_server()