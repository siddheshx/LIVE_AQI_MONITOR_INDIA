import asyncio
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import City, AQIReading
from app.services.aqi_service import fetch_multiple_cities


async def fetch_and_save_aqi():
    db = SessionLocal()

    try:
        # Step 1: Get all cities from PostgreSQL
        cities = db.scalars(
            select(City).order_by(City.id)
        ).all()

        if not cities:
            print("No cities found. Run seed_cities.py first.")
            return

        print(f"Fetching AQI data for {len(cities)} cities...")

        # Step 2: Fetch AQI data from Open-Meteo
        responses = await fetch_multiple_cities(cities)

        # Step 3: Verify API response count
        if len(responses) != len(cities):
            raise ValueError(
                f"Expected {len(cities)} responses, "
                f"but received {len(responses)}"
            )

        inserted = 0
        skipped = 0

        # Step 4: Process each city's AQI data
        for city, response in zip(cities, responses):

            current = response.get("current")

            if not current or not current.get("time"):
                skipped += 1
                print(f"Skipping {city.name}: missing current data")
                continue

            # Convert Open-Meteo's local time to timezone-aware IST
            observed_at = datetime.fromisoformat(
                current["time"]
            ).replace(
                tzinfo=ZoneInfo("Asia/Kolkata")
            )

            # Step 5: Check for duplicate readings
            existing = db.scalar(
                select(AQIReading).where(
                    AQIReading.city_id == city.id,
                    AQIReading.observed_at == observed_at,
                    AQIReading.source == "open-meteo",
                )
            )

            if existing:
                skipped += 1
                continue

            # Step 6: Create a new AQI reading
            reading = AQIReading(
                city_id=city.id,
                pm2_5=current.get("pm2_5"),
                pm10=current.get("pm10"),
                us_aqi=current.get("us_aqi"),
                european_aqi=current.get("european_aqi"),
                source="open-meteo",
                data_kind="modelled",
                observed_at=observed_at,
                fetched_at=datetime.now(timezone.utc),
            )

            db.add(reading)
            inserted += 1

        # Step 7: Save all readings to PostgreSQL
        db.commit()

        print("\n================================")
        print("AQI DATA COLLECTION COMPLETED")
        print("================================")
        print(f"Cities processed: {len(cities)}")
        print(f"New readings saved: {inserted}")
        print(f"Existing or skipped: {skipped}")
        print("================================")

    except Exception as error:
        db.rollback()
        print(f"Error while collecting AQI data: {error}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(fetch_and_save_aqi())