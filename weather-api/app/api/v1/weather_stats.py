from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud
from app.deps import get_db
from app.schemas import WeatherStatsOut

# Initialize API router for the Weather endpoints
router = APIRouter()


@router.get("/weather/stats", response_model=list[WeatherStatsOut])
def get_weather_stats(
    station_id: str = Query(None),
    year: int = Query(None),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    """
    Retrieves weather stats from the database.
    Optional filters - station_id and date, with support for pagination.
    """
    return crud.get_weather_stats(
        db, station_id=station_id, year=year, skip=skip, limit=limit
    )
