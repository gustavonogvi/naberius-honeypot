# Planning

## Overview
Build a basic honeypot (e.g.: SSH on port 22) that records connection attempts and displays a web dashboard with alerts and basic analyses.

The long-term goal is to evolve from a low interaction honeypot into a medium interaction honeypot — one that simulates a real SSH session, tricks attackers into revealing credentials, and feeds that data into a threat intelligence pipeline.

---

## EPIC 01 — Data Collection [done]

> Capture and store every connection attempt made to the honeypot.

**HU-01** [done] — As a analyst, I want the honeypot to listen on a fake port so that attackers connect to it without knowing it's a trap.

**HU-02** [done] — As a analyst, I want each connection attempt to be recorded with IP, timestamp, port, and payload so that I have raw data to analyse.

**HU-03** [done] — As a analyst, I want events to be persisted in SQLite so that data is not lost when the service restarts.

---

## EPIC 02 — Data Enrichment [done]

> Add context to raw events to make analysis more meaningful.

**HU-04** [done] — As a analyst, I want each IP to be enriched with country, city, and ASN so that I can understand where attacks are coming from.

**HU-05** [done] — As a analyst, I want geolocation to be fetched automatically when an event is saved so that I don't have to do it manually.

---

## EPIC 03 — API [done]

> Expose collected data through a REST API.


**HU-06** [done] — As a developer, I want a `GET /events` endpoint that returns all recorded events so that the dashboard can consume them.

**HU-07** [done] — As a developer, I want to be able to filter events by IP or date so that I can query specific attack windows.

---

## EPIC 04 — Dashboard [done]

> Visualize events and statistics in a web interface.

**HU-08** [done] — As a analyst, I want a page that lists all events in a table so that I can review them quickly.

**HU-09** [done] — As a analyst, I want basic statistics (total events, top IPs, top countries) so that I can identify patterns at a glance.

**HU-10** [done] — As a analyst, I want to filter the event list by IP or time range so that I can focus on a specific incident.

---

## EPIC 05 — Documentation and Safety [done]

> Make the project safe, understandable, and ready to present.

**HU-11** [done] — As a user, I want a README with setup instructions so that I can run the project from scratch.

**HU-12** [done] — As a user, I want documented risks and precautions so that I know how to run the honeypot safely.

---

## EPIC 06 — Medium Interaction [done]

> Evolve the honeypot from passive listener to active trap — simulate a real SSH session to collect credentials and attacker behavior.

**Context:** Right now the honeypot is a *low interaction* honeypot. It listens, sends a banner, and records what arrives. A real attacker or bot using an SSH client will not interact further — it expects a proper SSH handshake. A *medium interaction* honeypot fakes that handshake, lures the attacker into typing credentials, and captures everything.

**HU-13** [done] — As a analyst, I want the honeypot to perform a real SSH handshake using `paramiko` so that automated SSH clients (bots, scanners) connect fully instead of dropping the connection.

**HU-14** [done] — As a analyst, I want the server to present a fake login prompt so that attackers type their username and password.

**HU-15** [done] — As a analyst, I want every credential attempt (username + password) to be stored in the database so that I can build a list of real credentials used in the wild.

**HU-16** [done] — As a analyst, I want the login to always fail after a few attempts so that the attacker keeps trying and reveals more credential combinations.

**HU-17** [done] — As a analyst, I want the honeypot to record which SSH client and version the attacker is using so that I can fingerprint the tools they use.

**HU-18** [done] — As a analyst, I want the honeypot to compute a HASSH fingerprint from the client's SSH algorithm negotiation so that I can identify attack tools even when they spoof their version banner.

---

## EPIC 07 — Threat Intelligence (future)

> Turn raw events into actionable intelligence.

**Context:** Once we have enough data, the goal is to identify patterns — repeated IPs, credential spraying campaigns, botnets — and export that data in formats used by real SOC tools.

**HU-19** [done] — As a analyst, I want to flag IPs that made more than N attempts in a given time window so that I can identify brute force campaigns.

**HU-20** — As a analyst, I want to export the event list as CSV so that I can import it into tools like Splunk or Excel for further analysis.

**HU-21** [done] — As a analyst, I want to see the top 10 most attempted usernames and passwords so that I can understand what credentials attackers prioritize.

**HU-22** — As a analyst, I want to receive an alert when a new event arrives so that I don't have to keep the dashboard open to notice activity.

---

## Risks and Precautions
- Do not expose the honeypot in production without isolation.
- Respect local laws when collecting and storing IPs (LGPD in Brazil, GDPR in Europe).
- Avoid storing real credentials in plain text — hash or redact if needed.
- Do not run as root. Use ports above 1024 and a non-privileged user.
- If deploying to a cloud VM, isolate it completely from other services.
