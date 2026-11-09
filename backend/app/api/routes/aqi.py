from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.city import City
from app.models.aqi_reading import AQIReading
from app.services.aqi_service import fetch_multiple_cities


router = APIRouter()


# --------------------------------------------------
# GET ALL CITIES
# --------------------------------------------------

@router.get("/cities")
def get_cities(db: Session = Depends(get_db)):

    cities = db.scalars(
        select(City).order_by(City.name)
    ).all()

    return {
        "total_cities": len(cities),
        "cities": [
            {
                "id": city.id,
                "name": city.name,
                "state": city.state,
                "latitude": city.latitude,
                "longitude": city.longitude,
            }
            for city in cities
        ],
    }


# --------------------------------------------------
# GET LATEST AQI READINGS
# --------------------------------------------------

@router.get("/aqi/latest")
def get_latest_aqi(db: Session = Depends(get_db)):

    latest_times = (
        select(
            AQIReading.city_id,
            func.max(AQIReading.observed_at).label("latest_time"),
        )
        .group_by(AQIReading.city_id)
        .subquery()
    )

    results = db.execute(
        select(AQIReading, City)
        .join(City, AQIReading.city_id == City.id)
        .join(
            latest_times,
            (AQIReading.city_id == latest_times.c.city_id)
            & (AQIReading.observed_at == latest_times.c.latest_time),
        )
        .order_by(AQIReading.us_aqi.desc().nullslast())
    ).all()

    readings = []

    for reading, city in results:
        readings.append({
            "city": city.name,
            "state": city.state,
            "pm2_5": reading.pm2_5,
            "pm10": reading.pm10,
            "us_aqi": reading.us_aqi,
            "european_aqi": reading.european_aqi,
            "observed_at": reading.observed_at.isoformat(),
            "fetched_at": reading.fetched_at.isoformat(),
        })

    return {
        "total_cities": len(readings),
        "data_source": "Open-Meteo",
        "data_kind": "modelled",
        "readings": readings,
    }


# --------------------------------------------------
# GET AQI RANKINGS
# --------------------------------------------------

@router.get("/aqi/rankings")
def get_aqi_rankings(
    limit: int = Query(default=20, ge=1, le=103),
    db: Session = Depends(get_db),
):

    latest_times = (
        select(
            AQIReading.city_id,
            func.max(AQIReading.observed_at).label("latest_time"),
        )
        .group_by(AQIReading.city_id)
        .subquery()
    )

    results = db.execute(
        select(AQIReading, City)
        .join(City, AQIReading.city_id == City.id)
        .join(
            latest_times,
            (AQIReading.city_id == latest_times.c.city_id)
            & (AQIReading.observed_at == latest_times.c.latest_time),
        )
        .order_by(AQIReading.us_aqi.desc().nullslast())
        .limit(limit)
    ).all()

    rankings = []

    for rank, (reading, city) in enumerate(results, start=1):
        rankings.append({
            "rank": rank,
            "city": city.name,
            "state": city.state,
            "us_aqi": reading.us_aqi,
            "pm2_5": reading.pm2_5,
            "pm10": reading.pm10,
            "european_aqi": reading.european_aqi,
            "observed_at": reading.observed_at.isoformat(),
        })

    return {
        "total_ranked": len(rankings),
        "rankings": rankings,
    }


# --------------------------------------------------
# REFRESH AQI DATA
# --------------------------------------------------

@router.post("/aqi/refresh")
async def refresh_aqi_data(db: Session = Depends(get_db)):

    try:
        cities = db.scalars(
            select(City).order_by(City.id)
        ).all()

        if not cities:
            raise HTTPException(
                status_code=404,
                detail="No cities found in database.",
            )

        responses = await fetch_multiple_cities(cities)

        if len(responses) != len(cities):
            raise ValueError(
                f"Expected {len(cities)} responses, "
                f"received {len(responses)}",
            )

        inserted = 0
        updated = 0
        skipped = 0

        fetched_at = datetime.now(timezone.utc)

        for city, response in zip(cities, responses):

            current = response.get("current")

            if not current or not current.get("time"):
                skipped += 1
                continue

            observed_at = datetime.fromisoformat(
                current["time"]
            )

            if observed_at.tzinfo is None:
                observed_at = observed_at.replace(
                    tzinfo=ZoneInfo("Asia/Kolkata")
                )

            existing = db.scalar(
                select(AQIReading).where(
                    AQIReading.city_id == city.id,
                    AQIReading.observed_at == observed_at,
                    AQIReading.source == "open-meteo",
                )
            )

            values = {
                "pm2_5": current.get("pm2_5"),
                "pm10": current.get("pm10"),
                "us_aqi": current.get("us_aqi"),
                "european_aqi": current.get("european_aqi"),
                "fetched_at": fetched_at,
            }

            if existing:

                for key, value in values.items():
                    setattr(existing, key, value)

                updated += 1

            else:

                reading = AQIReading(
                    city_id=city.id,
                    source="open-meteo",
                    data_kind="modelled",
                    observed_at=observed_at,
                    **values,
                )

                db.add(reading)
                inserted += 1

        db.commit()

        return {
            "status": "success",
            "message": "AQI data refresh completed.",
            "cities_processed": len(cities),
            "new_readings_saved": inserted,
            "existing_readings_updated": updated,
            "skipped": skipped,
            "data_source": "Open-Meteo",
            "data_kind": "modelled",
            "fetched_at": fetched_at.isoformat(),
        }

    except HTTPException:
        raise

    except Exception as error:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"AQI refresh failed: {str(error)}",
        )