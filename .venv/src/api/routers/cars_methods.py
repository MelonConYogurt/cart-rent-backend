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


