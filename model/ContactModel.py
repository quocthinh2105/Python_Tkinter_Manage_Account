from utils.Database_connection import Database

class ContactModels:
    def __init__(self, id, contact_name, email, phone):
        self.id = id
        self.contact_name = contact_name
        self.email = email
        self.phone = phone

    @staticmethod
    def get_list_contact(username):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                query = "select id, contact_name, email, phone from contact where upper(user_name) = upper(%s) and unfriend = 0 order by created_at desc;"
                cursor.execute(query, (username,))
                result = cursor.fetchall()
                return [ContactModels(*data) for data in result]
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if conn:
                Database.release_connection(conn)

    @staticmethod
    def find_contact(username, contact_name):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                query = """
                            select u.id, u.username AS contact_name, u.email, u.phone from users u
                            where u.username like %s 
                            and upper(u.username) not in (select upper(c.contact_name) from contact c where upper(c.user_name) = upper(%s))
                            and upper(u.username) <> upper(%s)
                            order by u.created_at desc
                        """
                cursor.execute(query, (f"%{contact_name}%", username, username))
                result = cursor.fetchall()
                return [ContactModels(*data) for data in result]
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if conn:
                Database.release_connection(conn)

    @staticmethod
    def add_contact(username, contact_name, email, phone):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                query = "INSERT INTO contact (contact_name, email, phone, user_name) VALUES (upper(%s), %s, %s, upper(%s));"
                cursor.execute(query, (contact_name, email, phone, username))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            if conn:
                Database.release_connection(conn)