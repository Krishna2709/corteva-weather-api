from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import WeatherData


def check_weather_data():
    db: Session = SessionLocal()
    try:
        count = db.query(WeatherData).count()
        print(f"Total records in weather_data: {count}")

        records = db.query(WeatherData).limit(10).all()
        for record in records:
            print(record)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    check_weather_data()
