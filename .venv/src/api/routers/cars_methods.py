# from fastapi import APIRouter
from typing import List, Optional
import strawberry

#impor models for cars
from ..models.cars_models import *

#import database conection
from ...database.connect import Connect

@strawberry.type
class Query:
    @strawberry.field(description="Get all cars information", name="data")
    def get_all_cars_info(self, filters: Optional[CarFilterInput] = None, limit: int = 2, offset: int = 0) -> CarResponse:
        try:
            print("En la api:", limit, offset)
            db = Connect()
            if filters:
                data, total_rows = db.get_all_table_cars_info(filters, limit, offset)
            else:
                data, total_rows = db.get_all_table_cars_info(limit=limit, offset=offset)
        except Exception as e:
            print(e)
            return CarResponse(
            cars= [],
            total_rows= 0
        )
        finally:
            db.close()
        return CarResponse(
            cars=data,
            total_rows= total_rows
        )

@strawberry.type(description="Add new car info to the database")
class Mutation:
    @strawberry.mutation
    def add_new_car_info(self, car_model_input: CarModelInput) -> CarModel:
        try:
            db = Connect()
            response = db.insert_new_car_info(car_model_input)
            if response:
                return car_model_input
            else:
                raise Exception("Error adding new car info")
        except Exception as e:
            raise Exception(f"Error adding new car info: {e}")
        finally:
            db.close()
            
    
schema = strawberry.Schema(query= Query, mutation= Mutation, subscription=None)


