from utils.Database_connection import Database
from utils.Bcrypt_utils import hash_password

class UserModels:
    def __init__(self, id, username, password, email, phone):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone

    @staticmethod
    def validate_user(username):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                query = "SELECT id, username, password, email, phone FROM users WHERE username = upper(%s) limit 1;"
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                if result:
                    user = UserModels(result[0], result[1], result[2], result[3], result[4])
                    return user
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if conn:
                Database.release_connection(conn)

    @staticmethod
    def find_user(username, email):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                query = "SELECT id, username, password, email, phone FROM users WHERE username = upper(%s) and email = %s limit 1;"
                cursor.execute(query, (username, email,))
                result = cursor.fetchone()
                if result:
                    user = UserModels(result[0], result[1], result[2], result[3], result[4])
                    return user
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if conn:
                Database.release_connection(conn)
    
    @staticmethod
    def create_user(username, password, email, phone):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, password, email, phone) VALUES (upper(%s), %s, %s, %s)", 
                    (username, hash_password(password), email, phone)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            if conn:
                Database.release_connection(conn)
    
    @staticmethod
    def reset_pass(username, email):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "update users set password = %s where username = upper(%s) and email = %s", 
                    (hash_password("123456a@"), username, email)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            if conn:
                Database.release_connection(conn)
    
    @staticmethod
    def update_user(username, password, email, phone):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "update users set password = %s, email = %s, phone = %s where username = upper(%s)", 
                    (hash_password(password), email, phone, username)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            if conn:
                Database.release_connection(conn)