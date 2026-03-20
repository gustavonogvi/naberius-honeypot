# Planning

## Overview
Build a basic honeypot (e.g.: SSH on port 22) that records connection attempts and displays a web dashboard with alerts and basic analyses.

---

## EPIC 01 — Data Collection

> Capture and store every connection attempt made to the honeypot.

**HU-01** — As a analyst, I want the honeypot to listen on a fake port so that attackers connect to it without knowing it's a trap.

**HU-02** — As a analyst, I want each connection attempt to be recorded with IP, timestamp, port, and payload so that I have raw data to analyse.

**HU-03** — As a analyst, I want events to be persisted in SQLite so that data is not lost when the service restarts.

---

## EPIC 02 — Data Enrichment

> Add context to raw events to make analysis more meaningful.

**HU-04** — As a analyst, I want each IP to be enriched with country, city, and ASN so that I can understand where attacks are coming from.

**HU-05** — As a analyst, I want geolocation to be fetched automatically when an event is saved so that I don't have to do it manually.

---

## EPIC 03 — API

> Expose collected data through a REST API.

**HU-06** — As a developer, I want a `GET /events` endpoint that returns all recorded events so that the dashboard can consume them.

**HU-07** — As a developer, I want to be able to filter events by IP or date so that I can query specific attack windows.

---

## EPIC 04 — Dashboard

> Visualize events and statistics in a web interface.

**HU-08** — As a analyst, I want a page that lists all events in a table so that I can review them quickly.

**HU-09** — As a analyst, I want basic statistics (total events, top IPs, top countries) so that I can identify patterns at a glance.

**HU-10** — As a analyst, I want to filter the event list by IP or time range so that I can focus on a specific incident.

---

## EPIC 05 — Documentation and Safety

> Make the project safe, understandable, and ready to present.

**HU-11** — As a user, I want a README with setup instructions so that I can run the project from scratch.

**HU-12** — As a user, I want documented risks and precautions so that I know how to run the honeypot safely.

---

## Risks and Precautions
- Do not expose the honeypot in production without isolation.
- Respect local laws when collecting and storing IPs.
- Avoid storing real credentials.
