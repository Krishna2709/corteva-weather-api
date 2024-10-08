from fastapi import FastAPI

from app.api.v1 import weather, weather_stats
from app.database import engine
from app.models import Base

app = FastAPI()

# Ensure tables creation in the database
Base.metadata.create_all(bind=engine)

# Routers for the API
app.include_router(weather.router, prefix="/api/v1")
app.include_router(weather_stats.router, prefix="/api/v1")
