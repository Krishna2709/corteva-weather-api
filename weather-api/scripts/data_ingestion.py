import logging
import os
from datetime import datetime

import pandas as pd
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import WeatherData, WeatherStation

# Configure logging to display information messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def insert_station(db: Session, station_id: str):
    """
    Inserts a weather station into the weather_station table if it doesn't already exist.
    This ensures that we only add new stations to the database.
    """
    try:
        # Create a new WeatherStation object and add it to the session
        station = WeatherStation(id=station_id)
        db.add(station)
        db.commit()  # Commit the changes to the database
        logger.info(f"Inserted station_id {station_id} into weather_station table.")
    except IntegrityError:
        # If the station already exists (IntegrityError), we rollback the transaction
        db.rollback()


def ingest_weather_data(file_path: str, station_id: str):
    """
    Reads a weather data file, processes it, and ingests the data into the database.
    It checks for existing records to avoid duplicates and only inserts new data.
    """
    db: Session = SessionLocal()
    try:
        # Ensure the weather station is added to the database before inserting weather data
        insert_station(db, station_id)

        # Log the start of the ingestion process
        start_time = datetime.now()
        logger.info(
            f"Starting data ingestion for station_id {station_id} at {start_time}"
        )

        # Read the weather data from the file into a DataFrame
        data = pd.read_csv(
            file_path,
            delimiter="\t",  # Tab-separated values
            header=None,
            names=[
                "date",
                "max_temp",
                "min_temp",
                "precipitation",
            ],  # Define the column names
        )

        # Replace -9999 values with None (missing data)
        data.replace(-9999, None, inplace=True)

        # Convert the 'date' column from 'YYYYMMDD' format to a datetime object
        data["date"] = pd.to_datetime(data["date"], format="%Y%m%d", errors="coerce")

        # Drop rows where the 'date' is invalid (NaT)
        data.dropna(subset=["date"], inplace=True)

        # Fetch existing weather records for this station to avoid duplicate entries
        existing_records = (
            db.query(WeatherData).filter(WeatherData.station_id == station_id).all()
        )
        existing_dates = set([record.date for record in existing_records])

        # Prepare the weather data for insertion, avoiding duplicates
        weather_data_list = [
            WeatherData(
                station_id=station_id,
                date=row["date"],
                max_temp=row["max_temp"] if pd.notnull(row["max_temp"]) else None,
                min_temp=row["min_temp"] if pd.notnull(row["min_temp"]) else None,
                precipitation=(
                    row["precipitation"] if pd.notnull(row["precipitation"]) else None
                ),
            )
            for _, row in data.iterrows()
            if row["date"]
            not in existing_dates  # Only insert if the date doesn't already exist
        ]

        # Insert new records into the database if there are any
        if weather_data_list:
            db.bulk_save_objects(weather_data_list)
            db.commit()  # Commit the transaction
            logger.info(
                f"Inserted {len(weather_data_list)} new records for station_id {station_id}."
            )
        else:
            logger.info(f"No new records to insert for station_id {station_id}.")

        # Log the end of the ingestion process
        end_time = datetime.now()
        logger.info(
            f"Data ingestion completed for station_id {station_id} at {end_time}"
        )
        logger.info(f"Total ingestion time: {end_time - start_time}")

    except Exception as e:
        # Log any errors and roll back the transaction
        logger.error(f"An error occurred during ingestion: {e}")
        db.rollback()
    finally:
        # Close the database session
        db.close()


def ingest_all_files_in_directory(directory_path: str):
    """
    Processes all .txt files in the specified directory.
    Each file contains weather data for a different station, and the station ID is extracted from the file name.
    """
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):  # Only process .txt files
            # Extract station ID from the file name (without the extension)
            station_id = file_name.split(".")[0]

            # Create the full file path
            file_path = os.path.join(directory_path, file_name)

            # Ingest the weather data from the file
            ingest_weather_data(file_path, station_id)


if __name__ == "__main__":
    """
    process all weather data files in the specified directory.
    """
    directory_path = "/Users/krishna/Desktop/corteva/code-challenge-template-main/wx_data"  # Path to the directory containing weather files
    ingest_all_files_in_directory(directory_path)
