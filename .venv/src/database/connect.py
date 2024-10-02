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
    
    def get_all_table_cars_info(self)-> List[CarModelWithId]:
        cars_list = []
        try:
            query = "SELECT * FROM public.cars_info"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            for row in rows:
                car = CarModelWithId(
                    id=int(row[0]),
                    brand=str(row[1]),
                    model=str(row[2]),
                    year=int(row[3]),
                    color=str(row[4]),
                    mileage=int(row[5]),
                    number_of_doors=int(row[6]),
                    horse_power=int(row[7]),
                    torque=int(row[8]),
                    media_url=str(row[9]),
                    fuel_type=str(row[10]),
                    transmission_type=str(row[11]),
                    drive_type=str(row[12]),
                    body_type=str(row[13]),
                    vin=str(row[14])
                )
                cars_list.append(car)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
        finally:
            return cars_list

    def insert_new_car_info(self, brand: str, model: str, year: int, vin: str, color: str, mileage: int, number_of_doors: int, horse_power: int, torque: int, media_url: str, fuel_type: str, transmission_type: str, drive_type: str, body_type: str) -> bool:
        try:
            query = ("""
            INSERT INTO public.cars_info(
            brand, model, year, vin, color, mileage, number_of_doors, horse_power, torque, media_url, fuel_type, transmission_type, drive_type, body_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """)
            self.cursor.execute(query, (brand, model, year, vin, color, mileage, number_of_doors, horse_power, torque, media_url, fuel_type, transmission_type, drive_type, body_type))
            self.conn.commit()
            return True
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
            return False
        finally:
            self.close()

if __name__ == '__main__':
    pass

