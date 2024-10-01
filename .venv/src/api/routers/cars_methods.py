# from fastapi import APIRouter
# from typing import List

# #impor models for cars
# from ..models.cars_models import *

# #import database conection
# from ...database.connect import Connect

# router = APIRouter(
#     prefix= "/cars",
#     tags=["Cars methods"],
# )

# @router.post("/add/new/car/info",  response_model= CarModel)
# async def add_new_car_info(info: CarModel):
#     try:
#         db = Connect()
#         db.insert_new_car_info(
#             brand= info.brand,
#             model= info.model,
#             year= info.year,
#             vin= info.vin,
#             color= info.color,
#             mileage=info.mileage,
#             number_of_doors= info.number_of_doors,
#             horse_power= info.horse_power,
#             torque= info.torque,
#             media_url= info.media_url,
#             fuel_type= info.fuel_type,
#             transmission_type= info.transmission_type,
#             drive_type= info.drive_type,
#             body_type= info.body_type,
#         )
#     except Exception as e:
#         print(e)
#     finally:
#         return info
    
    
# @router.get("/get/all/cars/info",  response_model= List[CarModelWithId])
# async def get_all_cars_info():
#     try:
#         db = Connect()
#         data = db.get_all_table_cars_info()
#     except Exception as e:
#         print(e)
#     finally:
#         return data

import strawberry
from typing import List, Optional
from ..models.cars_models import CarModel, CarModelWithId
from ...database.connect import Connect

import strawberry
from typing import List, Optional
from ..models.cars_models import CarModelWithId
from ...database.connect import Connect

@strawberry.type
class Query:
    @strawberry.field
    def all_cars(self) -> List[CarModelWithId]:
        try:
            db = Connect()
            cars = db.get_all_table_cars_info()
            
            # Convertir los diccionarios a instancias de CarModelWithId
            car_objects = [CarModelWithId(**car) for car in cars]
            return car_objects
        except Exception as e:
            print(e)
            return []

    @strawberry.field
    def car_by_id(self, id: int) -> Optional[CarModelWithId]:
        try:
            db = Connect()
            car = next((car for car in db.get_all_table_cars_info() if car['id'] == id), None)
            return CarModelWithId(**car) if car else None
        except Exception as e:
            print(e)
            return None

# Resolver para agregar un nuevo coche
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_new_car(self, info: CarModel) -> CarModel:
        try:
            db = Connect()
            db.insert_new_car_info(
                brand=info.brand,
                model=info.model,
                year=info.year,
                vin=info.vin,
                color=info.color,
                mileage=info.mileage,
                number_of_doors=info.number_of_doors,
                horse_power=info.horse_power,
                torque=info.torque,
                media_url=info.media_url,
                fuel_type=info.fuel_type,
                transmission_type=info.transmission_type,
                drive_type=info.drive_type,
                body_type=info.body_type,
            )
            return info
        except Exception as e:
            print(e)
            return info

schema = strawberry.Schema(query=Query, mutation=Mutation)

