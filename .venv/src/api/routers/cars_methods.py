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
        return []
    finally:
        db.close()
    return data

@strawberry.type
class Query:
    data: List[CarModelWithId] = strawberry.field(resolver=get_all_cars_info)
    
    
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_new_car_info(self, car_model_input: CarModelInput) -> CarModel:
        try:
            db = Connect()
            response = db.insert_new_car_info(
                brand=car_model_input.brand,
                model=car_model_input.model,
                year=car_model_input.year,
                vin=car_model_input.vin,
                color=car_model_input.color,
                mileage=car_model_input.mileage,
                number_of_doors=car_model_input.number_of_doors,
                horse_power=car_model_input.horse_power,
                torque=car_model_input.torque,
                media_url=car_model_input.media_url,
                fuel_type=car_model_input.fuel_type,
                transmission_type=car_model_input.transmission_type,
                drive_type=car_model_input.drive_type,
                body_type=car_model_input.body_type,
            )
            if response:
                return car_model_input
            else:
                raise Exception(f"Error adding new car info: {e}")
        except Exception as e:
            raise Exception(f"Error adding new car info: {e}")
        finally:
            db.close()

    
schema = strawberry.Schema(query= Query, mutation= Mutation, subscription=None)


