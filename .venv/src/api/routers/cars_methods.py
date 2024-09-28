from fastapi import APIRouter

#impor models for cars
from ..models.cars_models import *

#import database conection
from ...database.connect import Connect

router = APIRouter(
    prefix= "/cars",
    tags=["Cars methods"],
   
)

@router.post("/add/new/car/info",  response_model= CarModel)
async def add_new_car_info(info: CarModel):
    try:
        db = Connect()
        db.insert_new_car_info(
            brand= info.brand,
            model= info.model,
            year= info.year,
            vin= info.vin,
            color= info.color,
            mileage=info.mileage,
            number_of_doors= info.number_of_doors,
            horse_power= info.horse_power,
            torque= info.torque,
            media_url= info.media_url,
            fuel_type= info.fuel_type,
            transmission_type= info.transmission_type,
            drive_type= info.drive_type,
            body_type= info.body_type,
        )
    except Exception as e:
        print(e)
    finally:
        return info



