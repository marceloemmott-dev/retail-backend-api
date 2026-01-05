from fastapi import FastAPI

app = FastAPI(title="Retail Backend API", description="Backend universal para retail y POS", version="0.1.0")


@app.get("/")
def health_check():
    return {"status": "ok"}
