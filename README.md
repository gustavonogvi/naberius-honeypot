# honeypot

A fake SSH server that logs connection attempts and stores them with geolocation data. Built as a portfolio project while studying Blue Team / SOC fundamentals.

## what it does

Runs a medium interaction SSH honeypot on port 2222. It performs a real SSH handshake using `paramiko`, presents a fake login prompt, and captures credentials — username, password, SSH client version, and HASSH fingerprint — from anyone who connects. All events are enriched with geolocation data and stored in SQLite. A web dashboard reads from the API and displays everything in real time.

The logo is an incomplete arc. The attacker never completes the cycle.

## how it works

```
attacker connects to port 2222
        ↓
real SSH handshake (paramiko — RSA key, algorithm negotiation)
        ↓
server banner: SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6
        ↓
HASSH fingerprint computed from client's algorithm negotiation (kex;enc;mac;compression → MD5)
        ↓
attacker types username + password
        ↓
login always fails — credentials captured silently
        ↓
geolocation API enriches the source IP (country, city, ASN)
        ↓
event saved to SQLite (ip, credentials, client version, HASSH, geo)
        ↓
dashboard reads from API and displays everything
```

## stack

- Python — core server, database, API
- paramiko — SSH protocol implementation (handshake, auth handling)
- SQLite — local event storage, no external database needed
- Flask — REST API that serves the events as JSON
- ip-api.com — free geolocation API, no key required
- HTML/CSS/JS — dashboard, no framework

## requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (package manager)

## setup

```bash
# clone the repo
git clone https://github.com/gustavonogvi/honeypot.git
cd honeypot

# create virtual environment and install dependencies
uv venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # Linux/Mac

uv sync

# initialize the database
python db/init_db.py
```

## running

You need three terminals open at the same time.

**Terminal 1 — honeypot server:**
```bash
python honeypot/server.py
```

**Terminal 2 — API:**
```bash
python api/app.py
```

**Terminal 3 — test a connection (optional):**
```bash
ssh -p 2222 -o StrictHostKeyChecking=no testuser@localhost
```

Then open `dashboard/index.html` in your browser.

## project structure

```
honeypot/
├── honeypot/
│   └── server.py       # fake SSH server, captures attempts
├── db/
│   └── init_db.py      # creates the SQLite schema
├── api/
│   └── app.py          # Flask API, exposes /events
├── dashboard/
│   └── index.html      # web dashboard
├── data/
│   └── honeypot.db     # generated at runtime, gitignored
├── pyproject.toml
└── README.md
```

## api

`GET /events` — returns all recorded events ordered by most recent.

```json
[
  {
    "id": 1,
    "ip": "1.2.3.4",
    "port": 2222,
    "timestamp": "2026-03-20T19:17:36.632995",
    "payload": "SSH-2.0-libssh2_1.10.0",
    "country": "China",
    "city": "Beijing",
    "region": "Beijing",
    "asn": "AS4134 Chinanet",
    "username": "root",
    "password": "123456",
    "client_version": "SSH-2.0-libssh2_1.10.0",
    "hassh": "a2de0f306611e0957be704f5b0e35a82",
    "hassh_algorithms": "curve25519-sha256,...;aes128-ctr,...;hmac-sha2-256,...;none,..."
  }
]
```

## risks and precautions

**Do not run this on a public IP without understanding what you're doing.**

- The honeypot is passive — it only listens and records. It does not attack back.
- Exposing port 2222 to the internet will attract real bots and scanners within minutes. That's the point, but it means real traffic hitting your machine.
- Do not run as root. Use a non-privileged user and a port above 1024.
- IPs collected are real. Depending on your country, storing IP addresses may fall under privacy laws (LGPD in Brazil, GDPR in Europe). Use this for research purposes only.
- Never store real credentials in the database or logs.
- If running on a cloud VM, isolate it — do not run alongside anything you care about.

## what i learned

- How TCP sockets work at a low level in Python
- How the SSH protocol works: handshake, key exchange, authentication flow
- How to implement a server-side SSH interface with paramiko
- How HASSH fingerprinting works: hashing the client's algorithm negotiation (KEXINIT) to identify tools even when they spoof version banners
- How geolocation APIs enrich network data
- The basic data flow of a SIEM: collect → enrich → store → visualize
- Why honeypots are useful for threat intelligence and credential collection
