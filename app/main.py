from fastapi import FastAPI

app = FastAPI(
    title="Financial Market Data Warehouse",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Financial Market Data Warehouse API",
        "status": "running"
    }
