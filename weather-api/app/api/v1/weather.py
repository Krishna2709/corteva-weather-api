from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, deps
from app.schemas import WeatherDataOut

# Initialize API router for the Weather endpoints
router = APIRouter()


@router.get("/weather/", response_model=list[WeatherDataOut])
def read_weather(
    station_id: str = Query(None),
    date: str = Query(None),
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 10,
):
    """
    Retrieves weather data from the database.
    Optional filters - station_id and date, with support for pagination.
    """

    return crud.get_weather_data(
        db, station_id=station_id, date=date, skip=skip, limit=limit
    )
