import psycopg2
from config import load_config
from utils.hashed_password import get_password_hash


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

    def get_all_table_cars_info(self):
        try:
            query = "SELECT * FROM public.cars_info"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            print("Table cars:\n", rows)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

    def create_user_for_api(self, username: str, full_name: str, email: str, password: str, disabled: bool):
        user_id = None  # Inicializa el user_id
        try:
            hashed_password = get_password_hash(password)
            if hashed_password:
                query = ("INSERT INTO public.users(username, full_name, email, hashed_password, disabled) "
                         "VALUES (%s, %s, %s, %s, %s) RETURNING id")
                self.cursor.execute(query, (username, full_name, email, hashed_password, disabled))
                user_id = self.cursor.fetchone()[0]
                self.conn.commit()  # Confirma los cambios en la base de datos
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
        

    


if __name__ == '__main__':
    db = Connect()
    users = db.get_all_users_api()
    print(users)
    db.close()
