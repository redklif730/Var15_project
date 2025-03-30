from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

# Create a base class for declarative models
Base = declarative_base()

# --- SQLAlchemy Models ---
class AirlineDB(Base):
    __tablename__ = "airlines"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier (primary key)
    name = Column(String(255), nullable=False)  # Airline name
    code = Column(String(255), nullable=False, unique=True)  # Airline code (unique)

    # base_airport related to AirportDB
    base_airport_name = Column(String(255), ForeignKey("airports.name"))
    base_airport = relationship("AirportDB", back_populates="airlines")

    employee_count = Column(Integer, nullable=False)  # Number of employees
    is_actual = Column(Boolean, default=True)  # Flag to mark record as active
    updated_at = Column(DateTime, default=datetime.utcnow)  # Last update timestamp


class AirportDB(Base):
    __tablename__ = "airports"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier (primary key)
    name = Column(String(255), nullable=False, unique=True)  # Airport name (unique)
    runway_count = Column(Integer, nullable=False)  # Number of runways
    capacity = Column(Integer, nullable=False)  # Maximum number of aircraft that can be based
    is_actual = Column(Boolean, default=True)  # Flag to mark record as active
    updated_at = Column(DateTime, default=datetime.utcnow)  # Last update timestamp

    airlines = relationship("AirlineDB", back_populates="base_airport")
