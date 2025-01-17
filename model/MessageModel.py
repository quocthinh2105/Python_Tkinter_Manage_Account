from utils.Database_connection import Database

class MessageModels:
    def __init__(self, id, sender_id, receiver_id, message, created_at, app_name, acc_name, acc_pass_enc, key_enc):
        self.id = id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = message
        self.created_at = created_at
        self.app_name = app_name
        self.acc_name = acc_name
        self.acc_pass_enc = acc_pass_enc
        self.key_enc = key_enc

    @staticmethod
    def load_messages(user_name, contact_name):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                query = """
                            select messages.* 
                            from (
                                select m1.id, m1.sender_id, m1.receiver_id, m1.message, m1.created_at, ap.app_name, ap.acc_name, ap.acc_pass_enc, ap.key_enc
                                from messages m1 
                                left join account_pass ap on ap.id = CAST(NULLIF(m1.message, '') AS INTEGER)
                                where upper(m1.sender_id) = upper(%s) and upper(m1.receiver_id) = upper(%s)
                                union all
                                select m2.id, m2.sender_id, m2.receiver_id, m2.message, m2.created_at, ap.app_name, ap.acc_name, ap.acc_pass_enc, ap.key_enc
                                from messages m2 
                                left join account_pass ap on ap.id = CAST(NULLIF(m2.message, '') AS INTEGER)
                                where upper(m2.sender_id) = upper(%s) and upper(m2.receiver_id) = upper(%s)
                            ) AS messages
                            order by messages.created_at asc
                        """
                cursor.execute(query, (user_name, contact_name, contact_name, user_name))
                result = cursor.fetchall()
                return [MessageModels(*data) for data in result]
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if conn:
                Database.release_connection(conn)

    @staticmethod
    def check_new_messages(user_name, contact_name, last_check_time):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                query = """
                            select messages.* 
                            from (
                                select m1.id, m1.sender_id, m1.receiver_id, m1.message, m1.created_at, ap.app_name, ap.acc_name, ap.acc_pass_enc, ap.key_enc
                                from messages m1 
                                left join account_pass ap on ap.id = CAST(NULLIF(m1.message, '') AS INTEGER)
                                where upper(m1.sender_id) = upper(%s) and upper(m1.receiver_id) = upper(%s)
                                and m1.created_at > %s
                                union all
                                select m2.id, m2.sender_id, m2.receiver_id, m2.message, m2.created_at, ap.app_name, ap.acc_name, ap.acc_pass_enc, ap.key_enc
                                from messages m2 
                                left join account_pass ap on ap.id = CAST(NULLIF(m2.message, '') AS INTEGER)
                                where upper(m2.sender_id) = upper(%s) and upper(m2.receiver_id) = upper(%s)
                                and m2.created_at > %s
                            ) AS messages
                            order by messages.created_at asc
                        """
                cursor.execute(query, (user_name, contact_name, last_check_time, contact_name, user_name, last_check_time))
                result = cursor.fetchall()
                return [MessageModels(*data) for data in result]
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if conn:
                Database.release_connection(conn)

    @staticmethod
    def create_message(sender_id , receiver_id , message):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                query = "INSERT INTO messages (sender_id , receiver_id , message, created_at) VALUES (upper(%s), upper(%s), %s, (NOW() AT TIME ZONE 'Asia/Ho_Chi_Minh'));"
                cursor.execute(query, (sender_id , receiver_id , message))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            if conn:
                Database.release_connection(conn)
    
