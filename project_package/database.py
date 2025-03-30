from .models import Base


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#import psycopg2

# Define the database URL (replace with your actual database URL)
#DATABASE_URL = "sqlite:///./airport_management.db"  # Example: SQLite database
DATABASE_URL = "postgresql://Database_user:`U`\pe8R_s@192.168.3.35:5432/Network_technology_airport"


# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# --- Database Setup ---
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()