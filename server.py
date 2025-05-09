from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
from utils import SERPAPI_API_KEY, DEFAULT_IMAGE_URL  # import from utils.py
from pydantic import BaseModel

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict origins here if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AdLog(BaseModel):
    adType: str

@app.post("/api/log-impression")
async def log_impression(request: Request, ad: AdLog):
    # Try to get IP from headers (for proxied requests)
    forwarded = request.headers.get("x-forwarded-for")
    client_ip = forwarded.split(",")[0] if forwarded else request.client.host

    # Logging logic
    if client_ip.startswith("127.") or client_ip == "localhost":
        log_type = "[LOCAL]"
    elif client_ip.startswith("192.168.") or client_ip.startswith("10."):
        log_type = "[INTERNAL]"
    elif client_ip == "203.0.113.42":  # Replace with your specific IP
        log_type = "[SPECIFIC IP]"
    else:
        log_type = "[PUBLIC]"

    print(f"{log_type} Ad viewed from {client_ip}, type: {ad.adType}")
    return {"status": "logged"}

def search_image_url(query: str):
    try:
        params = {
            "engine": "google",
            "q": query,
            "tbm": "isch",
            "api_key": SERPAPI_API_KEY
        }
        response = requests.get('https://serpapi.com/search', params=params)
        response.raise_for_status()
        data = response.json()
        if 'images_results' in data and len(data['images_results']) > 0:
            return data['images_results'][0]['thumbnail']
    except Exception as e:
        print(f"Image search failed: {e}")
    return None

@app.get("/health-check")
async def get_health():
    try:
        return JSONResponse({
            "Health check status": "Success"
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/fact")
async def get_fact():
    try:
        fact_response = requests.get('https://uselessfacts.jsph.pl/random.json')
        fact_response.raise_for_status()
        fact_data = fact_response.json()
        fact_text = fact_data.get('text', 'No fact found')

        # image_url = search_image_url(fact_text)
        # if not image_url:
        image_url = DEFAULT_IMAGE_URL

        return JSONResponse(content={
            "fact": fact_text,
            "image_url": image_url
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
