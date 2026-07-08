import os
import logging
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("vit-ai")

app = FastAPI(
    title="VIT-AI",
    description="VIT Network AI/ML models — 13-model ensemble powering the Intelligence Oracle",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {"message": "VIT-AI Intelligence Oracle is online"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/ping")
async def ping():
    return "pong"

@app.get("/version")
async def version():
    return {"version": os.getenv("APP_VERSION", "0.1.0")}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
