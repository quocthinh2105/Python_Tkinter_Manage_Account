from utils.Database_connection import Database

class AccountModels:
    def __init__(self, id, user_name, app_name, acc_name, acc_pass, acc_pass_enc, key_enc, description, is_remove):
        self.id = id
        self.user_name = user_name
        self.app_name = app_name
        self.acc_name = acc_name
        self.acc_pass = acc_pass
        self.acc_pass_enc = acc_pass_enc
        self.key_enc = key_enc
        self.description = description
        self.is_remove = is_remove

    @staticmethod
    def get_list_account(username):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                query = "select id, user_name, app_name, acc_name, acc_pass, acc_pass_enc, key_enc, description, is_remove from account_pass ap where user_name = upper(%s) order by created_at desc;"
                cursor.execute(query, (username,))
                result = cursor.fetchall()
                return [AccountModels(*data) for data in result]
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if conn:
                Database.release_connection(conn)

    @staticmethod
    def create_account(user_name, app_name, acc_name, acc_pass, acc_pass_enc, key_enc, description):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                query = "INSERT INTO account_pass (user_name, app_name, acc_name, acc_pass, acc_pass_enc, key_enc, description) VALUES (upper(%s), %s, %s, %s, %s, %s, %s);"
                cursor.execute(query, (user_name, app_name, acc_name, acc_pass, acc_pass_enc, key_enc, description))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            if conn:
                Database.release_connection(conn)

    @staticmethod
    def find_account(accountId):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                query = "select id, user_name, app_name, acc_name, acc_pass, acc_pass_enc, key_enc, description, is_remove from account_pass ap where id = %s;"
                cursor.execute(query, (accountId,))
                result = cursor.fetchone()
                if result:
                    account = AccountModels(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8])
                    return account
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if conn:
                Database.release_connection(conn)

    @staticmethod
    def update_account(accountId, app_name, acc_name, acc_pass, acc_pass_enc, key_enc, description):
        conn = None
        try:
            conn = Database.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "update account_pass set app_name = %s, acc_name = %s, acc_pass = %s, acc_pass_enc = %s, key_enc = %s, description = %s where id = %s", 
                    (app_name, acc_name, acc_pass, acc_pass_enc, key_enc, description, accountId)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            if conn:
                Database.release_connection(conn)
