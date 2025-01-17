import psycopg
import psycopg_pool

class Database:
    _pool = None

    @staticmethod
    def init_pool():
        try:
            if Database._pool is None:
                Database._pool = psycopg_pool.ConnectionPool(
                    min_size=1,
                    max_size=10,
                    conninfo ="dbname=neondb user=neondb_owner password=krctFiBGX6u0 host=ep-green-unit-a14c16cr-pooler.ap-southeast-1.aws.neon.tech"
                    # conninfo ="dbname=postgres_db user=pgadmin password=admin host=10.56.66.59"
                )
        except psycopg.Error as e:
            print("Error initializing database connection pool:", e)
            raise

    @staticmethod
    def get_connection():
        if Database._pool is None:
            raise Exception("Database pool is not initialized")
        return Database._pool.getconn()

    @staticmethod
    def release_connection(conn):
        if Database._pool:
            Database._pool.putconn(conn)

    @staticmethod
    def close_pool():
        if Database._pool:
            Database._pool.close()
