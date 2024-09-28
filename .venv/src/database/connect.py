import psycopg2
from .config import load_config
from .utils.hashed_password import get_password_hash

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
    
    def get_all_table_cars_info(self):
        cars_list = []
        try:
            query = "SELECT * FROM public.cars_info"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            for row in rows:
                car = {
                    "id": row[0],
                    "brand": row[1],
                    "model": row[2],
                    "year": row[3],
                    "vin": row[4],
                    "color": row[5],
                    "mileage": row[6],
                    "number_of_doors": row[7],
                    "horse_power": row[8],
                    "torque": row[9],
                    "media_url": row[10],
                    "fuel_type": row[11],
                    "transmission_type": row[12],
                    "drive_type": row[13],
                    "body_type": row[14]
                }
                cars_list.append(car)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
        finally:
            return cars_list


    def insert_new_car_info(self, brand: str, model: str, year: int, vin: int, color: str, mileage: int, number_of_doors: int, horse_power: int, torque: int, media_url: str, fuel_type: str, transmission_type: str, drive_type: str, body_type: str):
        car_id = None  # Initialize car_id
        try:
            query = ("""
            INSERT INTO public.cars_info(
            brand, model, year, vin, color, mileage, number_of_doors, horse_power, torque, media_url, fuel_type, transmission_type, drive_type, body_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
                """)
            self.cursor.execute(query, (brand, model, year, vin, color, mileage, number_of_doors, horse_power, torque, media_url, fuel_type, transmission_type, drive_type, body_type))
            car_id = self.cursor.fetchone()[0]
            self.conn.commit()
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
        finally:
            print("New car info added:", car_id)
            return car_id

if __name__ == '__main__':
    pass

