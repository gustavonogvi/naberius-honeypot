# honeypot

A fake SSH server that logs connection attempts and stores them with geolocation data. Built as a portfolio project while studying Blue Team / SOC fundamentals.

## what it does

Runs a TCP server on port 2222 that pretends to be an SSH service. When someone connects, it sends back a real SSH banner and records the attempt — IP, timestamp, payload, country, city, and ASN — into a SQLite database.

Eventually it'll have a web dashboard to visualize the data.

## stack

- Python (sockets, sqlite3)
- Flask (API, in progress)
- SQLite
- ip-api.com for geolocation

## running locally

```bash
uv venv && .venv\Scripts\activate
uv sync
python db/init_db.py
python honeypot/server.py
```

Then connect with telnet to test:
```bash
telnet localhost 2222
```

## project structure

```
honeypot/       # the fake server
db/             # database setup
api/            # REST API (in progress)
dashboard/      # web interface (in progress)
data/           # sqlite database (gitignored)
```

## status

Core honeypot working. API and dashboard in progress.
