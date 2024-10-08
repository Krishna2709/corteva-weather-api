from datetime import date
from typing import Optional

from pydantic import BaseModel, validator


# Schema for outputting weather data.
# This schema ensures that data returned from the API follows this structure.
class WeatherDataOut(BaseModel):
    station_id: str  # The ID of the weather station.
    date: str  # The date of the weather data, returned as a string.
    max_temp: Optional[float]  # The maximum temperature for the day, optional.
    min_temp: Optional[float]  # The minimum temperature for the day, optional.
    precipitation: Optional[float]  # The precipitation for the day, optional.

    # This function ensures the date is formatted as a string (YYYY-MM-DD) if it is a date object.
    @validator("date", pre=True)
    def convert_date(cls, value):
        if isinstance(value, date):
            return value.strftime(
                "%Y-%m-%d"
            )  # Format date as string if it's a date object.
        return value

    # This configuration tells Pydantic to automatically convert ORM objects to the schema model.
    class Config:
        orm_mode = True


# Schema for outputting weather statistics data.
# This schema ensures that the calculated statistics follow this structure.
class WeatherStatsOut(BaseModel):
    station_id: str  # The ID of the weather station.
    year: int  # The year for which the statistics are calculated.
    avg_max_temp: Optional[
        float
    ]  # The average maximum temperature for the year, optional.
    avg_min_temp: Optional[
        float
    ]  # The average minimum temperature for the year, optional.
    total_precipitation: Optional[
        float
    ]  # The total precipitation for the year, optional.

    # This configuration tells Pydantic to automatically convert ORM objects to the schema model.
    class Config:
        orm_mode = True
