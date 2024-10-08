from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String

from app.database import Base


# This class represents the weather station table in the database.
# It stores information about different weather stations.
class WeatherStation(Base):
    __tablename__ = "weather_station"  # The name of the table in the database

    id = Column(
        String, primary_key=True, index=True
    )  # Unique identifier for the station (primary key)
    name = Column(String)  # Name of the weather station (optional, can be null)


# This class represents the weather data table in the database.
# It stores daily weather records for each station.
class WeatherData(Base):
    __tablename__ = "weather_data"  # The name of the table in the database

    id = Column(
        Integer, primary_key=True, index=True
    )  # Unique identifier for each weather record (primary key)
    station_id = Column(
        String, ForeignKey("weather_station.id")
    )  # Foreign key linking to the weather station
    date = Column(Date, index=True)  # Date of the weather record
    max_temp = Column(Float)  # Maximum temperature recorded on that day (in Celsius)
    min_temp = Column(Float)  # Minimum temperature recorded on that day (in Celsius)
    precipitation = Column(
        Float
    )  # Amount of precipitation recorded on that day (in millimeters)


# This class represents the weather statistics table in the database.
# It stores yearly weather statistics for each station.
class WeatherStats(Base):
    __tablename__ = "weather_stats"  # The name of the table in the database

    id = Column(
        Integer, primary_key=True, index=True
    )  # Unique identifier for each stats record (primary key)
    station_id = Column(
        String, ForeignKey("weather_station.id")
    )  # Foreign key linking to the weather station
    year = Column(Integer, index=True)  # Year of the weather stats
    avg_max_temp = Column(
        Float, nullable=True
    )  # Average maximum temperature for the year (nullable)
    avg_min_temp = Column(
        Float, nullable=True
    )  # Average minimum temperature for the year (nullable)
    total_precipitation = Column(
        Float, nullable=True
    )  # Total precipitation for the year (in centimeters, nullable)
