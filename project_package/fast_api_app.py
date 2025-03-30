from .models import AirportDB, AirlineDB
from .pydentic_validation_models import AirlineCreate, AirlineResponse, AirlineUpdate, AirportCreate, AirportResponse, AirportUpdate
from .database import get_db

from typing import List
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Request


from fastapi.responses import HTMLResponse  # For returning HTML #ADDED
from fastapi.templating import Jinja2Templates # For using templates #ADDED



# Инициализация FastAPI приложения
app = FastAPI()  # Using FastAPI for automatic data validation and OpenAPI docs
templates = Jinja2Templates(directory="templates") #Initialize jinja2 #ADDED

# --- API Endpoints ---
@app.post("/airlines/", response_model=AirlineResponse, status_code=201)  # Use FastAPI annotation
def create_airline(airline: AirlineCreate, db: Session = Depends(get_db)):
    """Creates a new airline."""
    # Check if the base airport exists
    airport = db.query(AirportDB).filter(AirportDB.name == airline.base_airport_name).first()
    if not airport:
        raise HTTPException(status_code=400, detail="Base airport does not exist.")

    db_airline = AirlineDB(**airline.dict())  # Create DB object from Pydantic model
    db.add(db_airline)
    db.commit()
    db.refresh(db_airline)
    return db_airline  # FastAPI automatically converts this to AirlineResponse

@app.get("/airlines/{airline_id}", response_model=AirlineResponse)  # Use FastAPI annotation
def read_airline(airline_id: int, db: Session = Depends(get_db)):
    db_airline = db.query(AirlineDB).filter(AirlineDB.id == airline_id).first()
    if db_airline is None:
        raise HTTPException(status_code=404, detail="Airline not found")
    return db_airline

@app.get("/airlines/", response_model=List[AirlineResponse])
def read_airlines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    airlines = db.query(AirlineDB).offset(skip).limit(limit).all()
    return airlines

@app.post("/airports/", response_model=AirportResponse, status_code=201)
def create_airport(airport: AirportCreate, db: Session = Depends(get_db)):
    """Creates a new airport."""
    db_airport = AirportDB(**airport.dict())  # Create DB object from Pydantic Model
    db.add(db_airport)
    db.commit()
    db.refresh(db_airport)
    return db_airport


@app.put("/airlines/{airline_id}", response_model=AirlineResponse)
def update_airline(airline_id: int, airline: AirlineUpdate, db: Session = Depends(get_db)):
    """Updates an existing airline."""
    db_airline = db.query(AirlineDB).filter(AirlineDB.id == airline_id).first()
    if db_airline is None:
        raise HTTPException(status_code=404, detail="Airline not found")

    # Update the airline attributes based on the provided data
    if airline.name is not None:
        db_airline.name = airline.name
    if airline.code is not None:
        # Check if the code already exists for other airlines
        existing_airline_with_code = db.query(AirlineDB).filter(AirlineDB.code == airline.code, AirlineDB.id != airline_id).first()
        if existing_airline_with_code:
            raise HTTPException(status_code=400, detail="Airline code already exists for another airline.")
        db_airline.code = airline.code
    if airline.base_airport_name is not None:
        # Check if the base airport exists
        airport = db.query(AirportDB).filter(AirportDB.name == airline.base_airport_name).first()
        if not airport:
            raise HTTPException(status_code=400, detail="Base airport does not exist.")
        db_airline.base_airport_name = airline.base_airport_name
    if airline.employee_count is not None:
        db_airline.employee_count = airline.employee_count

    db_airline.updated_at = datetime.utcnow()  # Update timestamp
    db.commit()
    db.refresh(db_airline)
    return db_airline

@app.delete("/airlines/{airline_id}", status_code=204)
def delete_airline(airline_id: int, db: Session = Depends(get_db)):
    """Deletes an airline."""
    db_airline = db.query(AirlineDB).filter(AirlineDB.id == airline_id).first()
    if db_airline is None:
        raise HTTPException(status_code=404, detail="Airline not found")

    db.delete(db_airline)
    db.commit()
    return  # 204 No Content - successful deletion







@app.get("/airports/{airport_id}", response_model=AirportResponse)
def read_airport(airport_id: int, db: Session = Depends(get_db)):
    airport = db.query(AirportDB).filter(AirportDB.id == airport_id).first()
    if airport is None:
        raise HTTPException(status_code=404, detail="Airport not found")
    return airport

@app.get("/airports/", response_model=List[AirportResponse])
def read_airports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    airports = db.query(AirportDB).offset(skip).limit(limit).all()
    return airports

@app.put("/airports/{airport_id}", response_model=AirportResponse)
def update_airport(airport_id: int, airport: AirportUpdate, db: Session = Depends(get_db)):
    """Updates an existing airport."""
    db_airport = db.query(AirportDB).filter(AirportDB.id == airport_id).first()
    if db_airport is None:
        raise HTTPException(status_code=404, detail="Airport not found")

    if airport.name is not None:
        existing_airport_with_name = db.query(AirportDB).filter(AirportDB.name == airport.name, AirportDB.id != airport_id).first()
        if existing_airport_with_name:
            raise HTTPException(status_code=400, detail="Airport name already exists for another airport.")
        db_airport.name = airport.name
    if airport.runway_count is not None:
        db_airport.runway_count = airport.runway_count
    if airport.capacity is not None:
        db_airport.capacity = airport.capacity

    db_airport.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_airport)
    return db_airport

@app.delete("/airports/{airport_id}", status_code=204)
def delete_airport(airport_id: int, db: Session = Depends(get_db)):
    """Deletes an airport, but only if it is not used as a base airport for any airlines."""
    db_airport = db.query(AirportDB).filter(AirportDB.id == airport_id).first()
    if db_airport is None:
        raise HTTPException(status_code=404, detail="Airport not found")

    # Check if any airlines use this airport as their base airport
    airlines_using_airport = db.query(AirlineDB).filter(AirlineDB.base_airport_name == db_airport.name).all()

    if airlines_using_airport:
        airline_ids = [airline.id for airline in airlines_using_airport] #Extract Ids
        raise HTTPException(status_code=400, detail=f"Cannot delete airport because it is used as a base airport for the following airlines: {airline_ids}")

    db.delete(db_airport)
    db.commit()
    return  # 204 No Content - successful deletion





# --- HTML Endpoints ---
@app.get("/", response_class=HTMLResponse) #Return HTML
async def read_root(request: Request):
    """Serves the index page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/airlines_ui", response_class=HTMLResponse) #Return HTML
async def list_airlines(request: Request, db: Session = Depends(get_db)):
    """Lists all airlines."""
    airlines = db.query(AirlineDB).all()
    return templates.TemplateResponse("airline_list.html", {"request": request, "airlines": airlines})


@app.get("/airports_ui", response_class=HTMLResponse)
async def list_airports(request: Request, db: Session = Depends(get_db)):
    """Lists all airports."""
    airports = db.query(AirportDB).all()
    return templates.TemplateResponse("airport_list.html", {"request": request, "airports": airports})
