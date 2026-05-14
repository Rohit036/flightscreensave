from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Serve frontend
@app.get("/")
async def serve_home():
    return FileResponse("app/static/index.html")


# Flight API endpoint
@app.get("/api/flights")
async def get_flights():
    url = "https://opensky-network.org/api/states/all?lamin=52.1&lomin=4.6&lamax=52.5&lomax=5.2"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    flights = []
    if data.get("states"):
        for s in data["states"]:
            if s[6] and s[5]:  # lat, lon
                flights.append({
                    "callsign": s[1].strip() if s[1] else "",
                    "lat": s[6],
                    "lon": s[5],
                    "heading": s[10]
                })

    return JSONResponse(flights)
