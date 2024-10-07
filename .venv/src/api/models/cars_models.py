from typing import Optional
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
    
@strawberry.type
class CarModelWithId(CarModel):
    id: int
    

@strawberry.type
class User():
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

