import socket
import threading
import time
import datetime
import sqlite3
import os
import requests
import paramiko

HOST = "0.0.0.0"
PORT = 2222
DB_PATH = "data/honeypot.db"
HOST_KEY_PATH = "data/host_key"
GEO_API = "http://ip-api.com/json/{}"
AUTH_FAIL_DELAY = 0.5

def load_or_generate_host_key():
    if os.path.exists(HOST_KEY_PATH):
        return paramiko.RSAKey(filename=HOST_KEY_PATH)
    else:
        key = paramiko.RSAKey.generate(2048)
        key.write_private_key_file(HOST_KEY_PATH)
        print(f"[*] RSA key generated: {HOST_KEY_PATH}")
        return key

def get_geo(ip):
    try:
        response = requests.get(GEO_API.format(ip), timeout=5)
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

def log_event(ip, port, payload, username=None, password=None, client_version=None):
    timestamp = datetime.datetime.now().isoformat()
    geo = get_geo(ip)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO events
           (ip, port, timestamp, payload, country, city, region, asn,
            username, password, client_version)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            ip, port, timestamp, payload,
            geo["country"], geo["city"], geo["region"], geo["asn"],
            username, password, client_version,
        )
    )
    conn.commit()
    conn.close()

    print(f"[{timestamp}] {ip} | {geo['country']} | user={username!r} pass={password!r}")


class FakeSSHServer(paramiko.ServerInterface):

    def __init__(self):
        self.captured_username = None
        self.captured_password = None

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        self.captured_username = username
        self.captured_password = password
        time.sleep(AUTH_FAIL_DELAY)
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"


def handle_connection(conn, addr, host_key):
    ip = addr[0]
    fake_server = FakeSSHServer()
    try:
        transport = paramiko.Transport(conn)
        transport.local_version = "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6"
        transport.add_server_key(host_key)
        transport.start_server(server=fake_server)
        time.sleep(2)

        client_version = transport.remote_version

        log_event(
            ip=ip,
            port=PORT,
            payload=client_version,
            username=fake_server.captured_username,
            password=fake_server.captured_password,
            client_version=client_version,
        )

    except Exception as e:
        print(f"[!] {ip} desconectou: {e}")
    finally:
        try:
            transport.close()
        except Exception:
            pass
        conn.close()


def start_server():
    host_key = load_or_generate_host_key()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen(13)
    print(f"[*] SSH server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_connection, args=(conn, addr, host_key))
        t.daemon = True
        t.start()


if __name__ == "__main__":
    start_server()
