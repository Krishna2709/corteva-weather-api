import pandas as pd
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import WeatherData, WeatherStats


def calculate_yearly_stats():
    # Create a database session
    db: Session = SessionLocal()

    try:
        # Fetch all weather data from the database
        weather_data = db.query(WeatherData).all()

        # Convert the weather data into a pandas DataFrame (a table-like structure)
        data = pd.DataFrame(
            [
                {
                    "station_id": record.station_id,  # Weather station ID
                    "date": record.date,  # Date of the weather record
                    "max_temp": record.max_temp,  # Maximum temperature
                    "min_temp": record.min_temp,  # Minimum temperature
                    "precipitation": record.precipitation,  # Precipitation amount
                }
                for record in weather_data  # Iterate through all records
            ]
        )

        # Convert the 'date' column to a proper datetime format
        data["date"] = pd.to_datetime(data["date"])

        # Extract the year from the 'date' column and create a new 'year' column
        data["year"] = data["date"].dt.year

        # Group the data by station ID and year, then calculate:
        # - The average maximum temperature for each year and station
        # - The average minimum temperature for each year and station
        # - The total precipitation for each year and station
        yearly_stats = (
            data.groupby(["station_id", "year"])
            .agg(
                avg_max_temp=("max_temp", "mean"),  # Average max temperature
                avg_min_temp=("min_temp", "mean"),  # Average min temperature
                total_precipitation=("precipitation", "sum"),  # Total precipitation
            )
            .reset_index()  # Convert the grouped data back into a normal table
        )

        # Replace any missing values (NaN) with None to handle them properly in the database
        yearly_stats = yearly_stats.where(pd.notnull(yearly_stats), None)

        # For each row of the yearly statistics, insert the data into the WeatherStats table
        for _, row in yearly_stats.iterrows():
            stats = WeatherStats(
                station_id=row["station_id"],  # Weather station ID
                year=row["year"],  # Year of the statistics
                avg_max_temp=row["avg_max_temp"],  # Average max temperature
                avg_min_temp=row["avg_min_temp"],  # Average min temperature
                total_precipitation=row["total_precipitation"] / 10,  # Convert mm to cm
            )
            db.add(stats)  # Add the record to the database

        # Commit the changes to the database
        db.commit()
        print("Yearly statistics calculated and inserted into the database.")

    except Exception as e:
        # If there's an error, roll back any changes to avoid corrupting the database
        db.rollback()
        print(f"An error occurred during analysis: {e}")

    finally:
        # Close the database session
        db.close()


if __name__ == "__main__":
    # Run the yearly statistics calculation function
    calculate_yearly_stats()
