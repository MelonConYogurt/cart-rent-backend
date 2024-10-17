from typing import Optional, List
from pydantic import BaseModel
from datetime import date
import strawberry

@strawberry.type
class CarModel:
    brand: str
    model: str
    year: int
    vin: str
    color: str
    mileage: int
    number_of_doors: int
    horse_power: int
    torque: int
    media_url: str
    fuel_type: str
    transmission_type: str
    drive_type: str
    body_type: str
    status: bool
    price: int
    available: bool
    rent_days: int
    last_service: str
    
@strawberry.input
class CarModelInput:
    brand: str
    model: str
    year: int
    vin: str
    color: str
    mileage: int
    number_of_doors: int
    horse_power: int
    torque: int
    media_url: str
    fuel_type: str
    transmission_type: str
    drive_type: str
    body_type: str
    price: int
    
@strawberry.input
class CarFilterInput:
    car_id: Optional[int] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    brand: Optional[str] = None
    color: Optional[str] = None
    fuel_type: Optional[str] = None
    transmission_type: Optional[str] = None
    drive_type: Optional[str] = None
    mileage_min: Optional[float] = None
    mileage_max: Optional[float] = None
    
@strawberry.type
class CarModelWithId(CarModel):
    id: int

@strawberry.type
class CarResponse:
    cars: List[CarModelWithId]
    total_rows : int
    
class DeleteMethod(BaseModel):
    id: int

class ResponseDeleteMethod(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    vin: str
    color: str
    mileage: int
    number_of_doors: int
    horse_power: int
    torque: int
    media_url: str
    fuel_type: str
    transmission_type: str
    drive_type: str
    body_type: str
    status: bool
    price: int
    available: bool
    rent_days: int
    last_service: date
    