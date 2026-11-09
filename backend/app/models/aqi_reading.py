from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AQIReading(Base):
    __tablename__ = "aqi_readings"

    __table_args__ = (
        UniqueConstraint(
            "city_id",
            "observed_at",
            "source",
            name="uq_aqi_city_time_source",
        ),
        Index("ix_aqi_city_observed_at", "city_id", "observed_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False,
    )

    pm2_5: Mapped[float | None] = mapped_column(Float, nullable=True)
    pm10: Mapped[float | None] = mapped_column(Float, nullable=True)

    us_aqi: Mapped[int | None] = mapped_column(Integer, nullable=True)
    european_aqi: Mapped[int | None] = mapped_column(Integer, nullable=True)

    source: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        default="open-meteo",
    )

    data_kind: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="modelled",
    )

    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    city: Mapped["City"] = relationship(
        "City",
        back_populates="readings",
    )