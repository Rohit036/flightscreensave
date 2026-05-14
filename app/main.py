from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def serve_home():
    return FileResponse("app/static/index.html")


@app.get("/api/flights")
async def get_flights():
    # Bigger area (Netherlands region)
    url = "https://opensky-network.org/api/states/all?lamin=51.5&lomin=3.0&lamax=53.5&lomax=6.5"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    flights = []

    if data.get("states"):
        for s in data["states"]:
            lon = s[5]
            lat = s[6]
            heading = s[10]

            if lat and lon:
                flights.append({
                    "callsign": (s[1] or "").strip(),
                    "lat": lat,
                    "lon": lon,
                    "heading": heading or 0
                })

    return JSONResponse(flights)
