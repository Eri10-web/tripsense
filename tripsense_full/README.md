# TripSense

Working starter website for a travel metasearch + AI trip planner.

## What works now
- global city/airport autocomplete
- search for flights / hotels / cars / activities
- AI-style trip builder block
- saved trips and price watches in the browser
- FastAPI backend endpoints
- single-command local run

## What is still mock, not live supplier data
- prices are simulated on the backend
- no real affiliate links yet
- no real provider credentials yet
- no login/database yet

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```bash
http://127.0.0.1:8000
```

## API endpoints
- `GET /api/health`
- `GET /api/locations/autocomplete?q=par`
- `POST /api/search`
- `POST /api/trip/build`
- `POST /api/watch`
- `GET /api/watch`

## To make it truly live
Replace mock search logic in `app/main.py` with provider adapters:
- Amadeus for city/airport autocomplete and flights
- Booking Demand API for hotels / cars / possibly flights
- Viator or another supplier for activities
- attach affiliate deep links
- add auth, database, and notifications
