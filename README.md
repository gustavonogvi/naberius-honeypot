# honeypot

A fake SSH server that logs connection attempts and stores them with geolocation data. Built as a portfolio project while studying Blue Team / SOC fundamentals.

## what it does

Runs a TCP server on port 2222 that pretends to be an SSH service. When someone connects, it sends back a real SSH banner and records the attempt — IP, timestamp, payload, country, city, and ASN — into a SQLite database. A web dashboard reads from the API and displays the events in real time.

The logo is an incomplete arc. The attacker never completes the cycle.

## how it works

```
attacker connects to port 2222
        ↓
server sends SSH banner (looks real)
        ↓
attacker sends data (username, password attempt, etc.)
        ↓
honeypot captures IP + payload + timestamp
        ↓
geolocation API enriches the IP (country, city, ASN)
        ↓
event saved to SQLite
        ↓
dashboard reads from API and displays everything
```

## stack

- Python — core server, database, API
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
telnet localhost 2222
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
    "payload": "root\r\n",
    "country": "China",
    "city": "Beijing",
    "region": "Beijing",
    "asn": "AS4134 Chinanet"
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
- How SSH identifies itself to clients (protocol banners)
- How geolocation APIs enrich network data
- The basic data flow of a SIEM: collect → enrich → store → visualize
- Why honeypots are useful for threat intelligence
