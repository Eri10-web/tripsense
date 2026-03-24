from __future__ import annotations

from pathlib import Path
from typing import Literal
import os
import random

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="TripSense", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_MODE = os.getenv("TRIPSENSE_DATA_MODE", "mock")  # mock | live

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

LOCATIONS = [
    {"code": "NYC", "city": "New York", "country": "USA", "label": "New York, USA", "airports": ["JFK", "EWR", "LGA"]},
    {"code": "MIA", "city": "Miami", "country": "USA", "label": "Miami, USA", "airports": ["MIA"]},
    {"code": "CHI", "city": "Chicago", "country": "USA", "label": "Chicago, USA", "airports": ["ORD", "MDW"]},
    {"code": "LAX", "city": "Los Angeles", "country": "USA", "label": "Los Angeles, USA", "airports": ["LAX"]},
    {"code": "SFO", "city": "San Francisco", "country": "USA", "label": "San Francisco, USA", "airports": ["SFO"]},
    {"code": "BOS", "city": "Boston", "country": "USA", "label": "Boston, USA", "airports": ["BOS"]},
    {"code": "LON", "city": "London", "country": "United Kingdom", "label": "London, United Kingdom", "airports": ["LHR", "LGW"]},
    {"code": "PAR", "city": "Paris", "country": "France", "label": "Paris, France", "airports": ["CDG", "ORY"]},
    {"code": "LIS", "city": "Lisbon", "country": "Portugal", "label": "Lisbon, Portugal", "airports": ["LIS"]},
    {"code": "BCN", "city": "Barcelona", "country": "Spain", "label": "Barcelona, Spain", "airports": ["BCN"]},
    {"code": "ROM", "city": "Rome", "country": "Italy", "label": "Rome, Italy", "airports": ["FCO", "CIA"]},
    {"code": "ATH", "city": "Athens", "country": "Greece", "label": "Athens, Greece", "airports": ["ATH"]},
    {"code": "AMS", "city": "Amsterdam", "country": "Netherlands", "label": "Amsterdam, Netherlands", "airports": ["AMS"]},
    {"code": "PRG", "city": "Prague", "country": "Czech Republic", "label": "Prague, Czech Republic", "airports": ["PRG"]},
    {"code": "DXB", "city": "Dubai", "country": "UAE", "label": "Dubai, UAE", "airports": ["DXB"]},
    {"code": "BKK", "city": "Bangkok", "country": "Thailand", "label": "Bangkok, Thailand", "airports": ["BKK"]},
    {"code": "TYO", "city": "Tokyo", "country": "Japan", "label": "Tokyo, Japan", "airports": ["HND", "NRT"]},
    {"code": "SIN", "city": "Singapore", "country": "Singapore", "label": "Singapore", "airports": ["SIN"]},
    {"code": "CUN", "city": "Cancun", "country": "Mexico", "label": "Cancun, Mexico", "airports": ["CUN"]},
    {"code": "MEX", "city": "Mexico City", "country": "Mexico", "label": "Mexico City, Mexico", "airports": ["MEX"]},
    {"code": "RIO", "city": "Rio de Janeiro", "country": "Brazil", "label": "Rio de Janeiro, Brazil", "airports": ["GIG"]},
    {"code": "CAI", "city": "Cairo", "country": "Egypt", "label": "Cairo, Egypt", "airports": ["CAI"]},
]

FLIGHTS = [
    {"id": "f1", "from": "NYC", "to": "LIS", "month": "May", "price": 540, "duration": "7h 05m", "stops": "Nonstop", "provider": "SkyRoute", "tag": "Best overall"},
    {"id": "f2", "from": "NYC", "to": "BCN", "month": "May", "price": 610, "duration": "8h 10m", "stops": "1 stop", "provider": "FlyNow", "tag": "Popular"},
    {"id": "f3", "from": "MIA", "to": "CUN", "month": "May", "price": 280, "duration": "2h 15m", "stops": "Nonstop", "provider": "AirDeals", "tag": "Budget"},
    {"id": "f4", "from": "NYC", "to": "PAR", "month": "June", "price": 690, "duration": "7h 40m", "stops": "Nonstop", "provider": "TripLines", "tag": "Premium"},
    {"id": "f5", "from": "CHI", "to": "ROM", "month": "May", "price": 640, "duration": "9h 15m", "stops": "1 stop", "provider": "TripLines", "tag": "Strong value"},
    {"id": "f6", "from": "NYC", "to": "ATH", "month": "May", "price": 720, "duration": "10h 05m", "stops": "1 stop", "provider": "SkyRoute", "tag": "Sunny pick"},
    {"id": "f7", "from": "BOS", "to": "LON", "month": "May", "price": 480, "duration": "6h 25m", "stops": "Nonstop", "provider": "FlyNow", "tag": "Value"},
    {"id": "f8", "from": "LAX", "to": "TYO", "month": "June", "price": 830, "duration": "11h 35m", "stops": "Nonstop", "provider": "PacificAir", "tag": "Long-haul"},
    {"id": "f9", "from": "SFO", "to": "SIN", "month": "June", "price": 915, "duration": "16h 10m", "stops": "Nonstop", "provider": "PacificAir", "tag": "Asia route"},
    {"id": "f10", "from": "NYC", "to": "DXB", "month": "June", "price": 940, "duration": "12h 15m", "stops": "Nonstop", "provider": "TripLines", "tag": "Luxury route"},
]

HOTELS = [
    {"id": "h1", "city": "LIS", "name": "Casa Aurora", "style": "Boutique", "area": "Baixa", "price": 145, "rating": 9.0, "provider": "StayHub", "tag": "Central"},
    {"id": "h2", "city": "LIS", "name": "Atlantic View Suites", "style": "Couples", "area": "Chiado", "price": 178, "rating": 9.3, "provider": "Booking Partner", "tag": "Romantic"},
    {"id": "h3", "city": "BCN", "name": "Casa Rambla", "style": "City", "area": "Eixample", "price": 166, "rating": 8.8, "provider": "StayHub", "tag": "Walkable"},
    {"id": "h4", "city": "CUN", "name": "Mar Azul Resort", "style": "Beach", "area": "Hotel Zone", "price": 190, "rating": 8.9, "provider": "BeachStay", "tag": "Beachfront"},
    {"id": "h5", "city": "PAR", "name": "Maison Lumiere", "style": "Luxury", "area": "Saint-Germain", "price": 235, "rating": 9.1, "provider": "Booking Partner", "tag": "Premium"},
    {"id": "h6", "city": "ROM", "name": "Trastevere House", "style": "Boutique", "area": "Trastevere", "price": 158, "rating": 8.9, "provider": "StayHub", "tag": "Neighborhood feel"},
    {"id": "h7", "city": "ATH", "name": "Acropolis Terrace", "style": "City", "area": "Plaka", "price": 149, "rating": 8.7, "provider": "TripRooms", "tag": "Historic core"},
    {"id": "h8", "city": "LON", "name": "Kensington Lane", "style": "City", "area": "South Kensington", "price": 212, "rating": 8.8, "provider": "Booking Partner", "tag": "Museum district"},
    {"id": "h9", "city": "TYO", "name": "Asakusa House", "style": "Boutique", "area": "Asakusa", "price": 172, "rating": 8.9, "provider": "StayHub", "tag": "Local feel"},
    {"id": "h10", "city": "DXB", "name": "Marina Glass Hotel", "style": "Luxury", "area": "Dubai Marina", "price": 260, "rating": 9.0, "provider": "TripRooms", "tag": "Skyline"},
]

CARS = [
    {"id": "c1", "city": "LIS", "company": "DriveGo", "type": "Compact", "daily": 38, "tag": "Best value"},
    {"id": "c2", "city": "BCN", "company": "CityWheel", "type": "Compact", "daily": 42, "tag": "City friendly"},
    {"id": "c3", "city": "CUN", "company": "SunCar", "type": "SUV", "daily": 54, "tag": "Beach trips"},
    {"id": "c4", "city": "ROM", "company": "ViaDrive", "type": "Economy", "daily": 36, "tag": "Low cost"},
    {"id": "c5", "city": "ATH", "company": "Aegean Cars", "type": "Compact", "daily": 40, "tag": "Island-ready"},
    {"id": "c6", "city": "LON", "company": "BritWheel", "type": "Compact", "daily": 55, "tag": "Urban use"},
]

ACTIVITIES = [
    {"id": "a1", "city": "LIS", "name": "Sunset food walk", "type": "Food", "price": 49, "provider": "GoExplore", "tag": "Couples"},
    {"id": "a2", "city": "LIS", "name": "Sintra day trip", "type": "Day trip", "price": 79, "provider": "TripFun", "tag": "Scenic"},
    {"id": "a3", "city": "BCN", "name": "Gaudi highlights tour", "type": "City", "price": 44, "provider": "GoExplore", "tag": "Top-rated"},
    {"id": "a4", "city": "CUN", "name": "Isla Mujeres boat day", "type": "Beach", "price": 88, "provider": "TripFun", "tag": "Popular"},
    {"id": "a5", "city": "ROM", "name": "Colosseum fast entry", "type": "Historic", "price": 39, "provider": "MusePass", "tag": "Skip line"},
    {"id": "a6", "city": "ATH", "name": "Acropolis evening tour", "type": "Historic", "price": 42, "provider": "MusePass", "tag": "Best seller"},
    {"id": "a7", "city": "LON", "name": "West End theatre ticket", "type": "Culture", "price": 72, "provider": "GoExplore", "tag": "Iconic"},
    {"id": "a8", "city": "TYO", "name": "Tokyo night food tour", "type": "Food", "price": 68, "provider": "TripFun", "tag": "Popular"},
    {"id": "a9", "city": "DXB", "name": "Desert safari", "type": "Adventure", "price": 74, "provider": "GoExplore", "tag": "Top pick"},
]

WATCHES: list[dict] = []


class SearchRequest(BaseModel):
    originCode: str | None = None
    destinationCode: str | None = None
    month: str | None = None
    travelers: int = Field(default=1, ge=1, le=12)
    nights: int = Field(default=5, ge=1, le=60)
    budget: int | None = Field(default=None, ge=0)
    vibe: str | None = None
    mode: Literal["ai", "flights", "hotels", "cars", "activities"] = "ai"


class WatchRequest(BaseModel):
    type: Literal["flight", "hotel"]
    refId: str
    target: float = Field(gt=0)
    email: str | None = None


@app.get("/")
def root() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "mode": DATA_MODE}


@app.get("/api/locations/autocomplete")
def autocomplete(q: str = Query(..., min_length=1)) -> list[dict]:
    query = q.strip().lower()
    results: list[dict] = []
    for item in LOCATIONS:
        hay = f"{item['city']} {item['country']} {item['label']} {item['code']} {' '.join(item['airports'])}".lower()
        if query in hay:
            results.append(item)
    return results[:8]


@app.post("/api/search")
def search(payload: SearchRequest) -> dict:
    flights = [
        {**item, "price": max(25, item["price"] + random.randint(-12, 10))}
        for item in FLIGHTS
        if (not payload.originCode or item["from"] == payload.originCode)
        and (not payload.destinationCode or item["to"] == payload.destinationCode)
        and (not payload.month or item["month"] == payload.month)
    ]
    flights.sort(key=lambda x: x["price"])

    hotels = [
        {**item, "price": max(25, item["price"] + random.randint(-8, 6))}
        for item in HOTELS
        if not payload.destinationCode or item["city"] == payload.destinationCode
    ]
    hotels.sort(key=lambda x: (x["price"], -x["rating"]))

    cars = [item for item in CARS if not payload.destinationCode or item["city"] == payload.destinationCode]
    cars.sort(key=lambda x: x["daily"])

    activities = [item for item in ACTIVITIES if not payload.destinationCode or item["city"] == payload.destinationCode]
    activities.sort(key=lambda x: x["price"])

    return {
        "source": DATA_MODE,
        "origin": next((x for x in LOCATIONS if x["code"] == payload.originCode), None),
        "destination": next((x for x in LOCATIONS if x["code"] == payload.destinationCode), None),
        "flights": flights,
        "hotels": hotels,
        "cars": cars,
        "activities": activities,
    }


@app.post("/api/trip/build")
def build_trip(payload: SearchRequest) -> dict:
    results = search(payload)
    destination = results["destination"]
    origin = results["origin"]
    best_flight = results["flights"][0] if results["flights"] else None
    best_hotel = results["hotels"][0] if results["hotels"] else None
    activities = results["activities"][:2]

    flight_total = (best_flight["price"] * payload.travelers) if best_flight else 0
    hotel_total = (best_hotel["price"] * payload.nights) if best_hotel else 0
    activity_total = sum(x["price"] for x in activities) * payload.travelers
    total = flight_total + hotel_total + activity_total

    return {
        "source": DATA_MODE,
        "headline": f"{destination['city'] if destination else payload.destinationCode} fits your trip request",
        "summary": "This plan is assembled by server-side logic and is ready to be replaced with real provider and AI integrations.",
        "estimatedTotal": total,
        "origin": origin,
        "destination": destination,
        "flightPrimary": best_flight,
        "stayPrimary": best_hotel,
        "activities": activities,
        "budgetStatus": "Within target budget" if payload.budget and total <= payload.budget else "Check budget alignment",
        "itinerary": [
            f"Day 1: depart from {origin['city'] if origin else payload.originCode} and arrive in {destination['city'] if destination else payload.destinationCode}.",
            "Day 2: city exploration and first core activity.",
            "Day 3: slower day with food and neighborhood discovery.",
            f"Day {max(4, payload.nights)}: flexible final day and departure planning.",
        ],
    }


@app.post("/api/watch")
def create_watch(payload: WatchRequest) -> dict:
    watch = payload.model_dump()
    watch["id"] = len(WATCHES) + 1
    WATCHES.append(watch)
    return {"ok": True, "watch": watch}


@app.get("/api/watch")
def list_watches() -> dict:
    return {"items": WATCHES}
