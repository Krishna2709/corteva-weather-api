from sqlalchemy.orm import Session

from app.models import WeatherData, WeatherStats


# Function to retrieve weather data from the database
# Can filter by station_id and date if provided
# Supports pagination using skip and limit
def get_weather_data(
    db: Session,
    station_id: str = None,  # Optional filter by station ID
    date: str = None,  # Optional filter by date
    skip: int = 0,  # Number of records to skip (for pagination)
    limit: int = 10,  # Maximum number of records to return (for pagination)
):
    query = db.query(WeatherData)  # Start the query on the WeatherData table

    # If station_id is provided, filter the query by station ID
    if station_id:
        query = query.filter(WeatherData.station_id == station_id)

    # If date is provided, filter the query by date
    if date:
        query = query.filter(WeatherData.date == date)

    # Apply pagination and return the results
    return query.offset(skip).limit(limit).all()


# Function to retrieve weather statistics from the database
# Can filter by station_id and year if provided
# Supports pagination using skip and limit
def get_weather_stats(
    db: Session,
    station_id: str = None,  # Optional filter by station ID
    year: int = None,  # Optional filter by year
    skip: int = 0,  # Number of records to skip (for pagination)
    limit: int = 10,  # Maximum number of records to return (for pagination)
):
    query = db.query(WeatherStats)  # Start the query on the WeatherStats table

    # If station_id is provided, filter the query by station ID
    if station_id:
        query = query.filter(WeatherStats.station_id == station_id)

    # If year is provided, filter the query by year
    if year:
        query = query.filter(WeatherStats.year == year)

    # Apply pagination and return the results
    return query.offset(skip).limit(limit).all()
