# from fastapi import APIRouter
from typing import List
import strawberry

#impor models for cars
from ..models.cars_models import *

#import database conection
from ...database.connect import Connect

@strawberry.type
class Query:
    @strawberry.field
    def get_all_cars_info(self, filters: Optional[CarFilterInput] = None) -> List[CarModelWithId]:
        try:
            db = Connect()
            if filters:
                data = db.get_all_table_cars_info(filters)
            else:
                data = db.get_all_table_cars_info()
        except Exception as e:
            print(e)
            return []
        finally:
            db.close()
        return data

    
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


# from typing import List, Optional
# import strawberry
# from fastapi import Depends

# # Importar los métodos de autorización de FastAPI
# from ..models.cars_models import *
# from ...database.connect import Connect
# from ..main import get_current_active_user  # Importa la función de autorización que verifica el JWT

# @strawberry.type
# class Query:
#     # Aquí aplicamos la autorización usando Depends y get_current_active_user
#     @strawberry.field
#     def get_all_cars_info(self, filters: Optional[CarFilterInput] = None, current_user: User = Depends(get_current_active_user)) -> List[CarModelWithId]:
#         try:
#             db = Connect()
#             if filters:
#                 data = db.get_all_table_cars_info(filters)
#             else:
#                 data = db.get_all_table_cars_info()
#         except Exception as e:
#             print(e)
#             return []
#         finally:
#             db.close()
#         return data

# @strawberry.type
# class Mutation:
#     # Requiere que el usuario esté autenticado antes de poder añadir información de un auto
#     @strawberry.mutation
#     def add_new_car_info(self, car_model_input: CarModelInput, current_user: User = Depends(get_current_active_user)) -> CarModel:
#         try:
#             db = Connect()
#             response = db.insert_new_car_info(car_model_input)
#             if response:
#                 return car_model_input
#             else:
#                 raise Exception("Error adding new car info")
#         except Exception as e:
#             raise Exception(f"Error adding new car info: {e}")
#         finally:
#             db.close()

# # Definir el esquema
# schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=None)
