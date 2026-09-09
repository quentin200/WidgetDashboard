from fastapi import FastAPI

from app.routers import dashboard
from app.routers.widgets import weather
#news, stocks, crypto, calendar, tasks

app = FastAPI()
app.include_router(dashboard.router)
app.include_router(weather.router)


@app.get("/")
def title():
    return {"message": "Personal Widget Dashboard API"}

@app.get("/health")
def status():
    return {"status": "OK"}