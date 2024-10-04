from typing import List
import psycopg2
from .config import load_config
from .utils.hashed_password import get_password_hash


#import models from strawberry types
from ..api.models.cars_models import *

class Connect:
    def __init__(self):
        """ Connect to the PostgreSQL database server """
        try:
            config = load_config()
            self.conn = psycopg2.connect(**config)
            print('Connected to the PostgreSQL server.')
            self.cursor = self.conn.cursor()
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
            
    def close(self):
        """ Close the cursor and connection """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            
            
    # -----------------------------------------------------------
    # users api Functions
    # -----------------------------------------------------------

    def create_user_for_api(self, username: str, full_name: str, email: str, password: str, disabled: bool):
        user_id = None  # Inicializa el user_id
        try:
            hashed_password = get_password_hash(password)
            if hashed_password:
                query = ("INSERT INTO public.users(username, full_name, email, hashed_password, disabled) "
                         "VALUES (%s, %s, %s, %s, %s) RETURNING id")
                self.cursor.execute(query, (username, full_name, email, hashed_password, disabled))
                user_id = self.cursor.fetchone()[0]
                self.conn.commit()
            else:
                print("Failed to hash the password.")
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

        finally:
            return user_id
        
    def get_all_users_api(self):
        users_in_db = {}
        try:
            query = "SELECT * FROM public.users"
            self.cursor.execute(query)
            users = self.cursor.fetchall()
            if users:
                for user in users:
                    users_in_db[user[1]] = {
                        "username": user[1],
                        "full_name": user[2],
                        "email": user[3],
                        "hashed_password": user[4],
                        "disabled": user[5]
                    }
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)   
        finally:
            return users_in_db        
    
    # -----------------------------------------------------------
    # Car Functions
    # -----------------------------------------------------------
    def get_all_table_cars_info(self, info: CarFilterInput) -> List[CarModelWithId]:
        cars_list = []
        try:
            query = "SELECT * FROM public.cars_info WHERE 1=1"
            query_params = []

            if info.car_id is not None:
                query += " AND id = %s"
                query_params.append(info.car_id)
            
            if info.price_min is not None and info.price_max is not None:
                query += " AND price >= %s AND price <= %s"
                query_params.append(info.price_min)
                query_params.append(info.price_max)
            
            if info.brand is not None:
                query += " AND brand = %s"
                query_params.append(info.brand)

            self.cursor.execute(query, tuple(query_params))
            rows = self.cursor.fetchall()

            columns_names = [desc[0] for desc in self.cursor.description]
            
            for row in rows:
                car_data = dict(zip(columns_names, row))
                car = CarModelWithId(**car_data)
                cars_list.append(car)

        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
        finally:
            return cars_list

            
    def insert_new_car_info(self, car_info: CarModelInput) -> bool:
        try:
            car_info_dict = vars(car_info)
            
            columns = ', '.join(car_info_dict.keys())
            values = tuple(car_info_dict.values())
            
            print(type(columns))
            query = f"""
            INSERT INTO public.cars_info ({columns})
            VALUES ({', '.join(['%s'] * len(values))});
            """
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except (psycopg2.DatabaseError, Exception) as error:
            print(f"Error: {error}")
            return False
        finally:
            self.close()

