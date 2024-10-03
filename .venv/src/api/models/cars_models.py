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
    
@strawberry.type
class CarModelWithId(CarModel):
    id: int
    