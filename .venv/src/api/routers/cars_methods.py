# from fastapi import APIRouter
from typing import List
import strawberry

#impor models for cars
from ..models.cars_models import *

#import database conection
from ...database.connect import Connect

def get_all_cars_info() -> List[CarModelWithId]:
    try:
        db = Connect()
        data = db.get_all_table_cars_info()
    except Exception as e:
        print(e)
    finally:
        return data

@strawberry.type
class Query:
    data: List[CarModelWithId] = strawberry.field(resolver=get_all_cars_info)
    
    
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_new_car_info(info: CarModel) -> CarModel:
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
    
    
schema = strawberry.Schema(query= Query, mutation= Mutation, subscription=None)


