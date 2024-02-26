import snowflake.connector
import pymysql

def connect_to_database_Mysql():
    try:
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'Syteme_Tutorat'
        }
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        print("Connexion à la base de données réussie.")
        return connection,cursor
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None, None
# connect to snowflake
def connect_to_snowflake():
    try:
        config = {
            "user": 'kassambara',
            "password": 'B@mako2021',
            "account": 'kdgvgef-hs83902',
            "database": 'Systeme_Tutorat',
            "schema": 'TUTORAT_SCHEMA',
        }
        conn = snowflake.connector.connect(**config)
        cursor = conn.cursor()
        print("Connected to Snowflake")
        return cursor
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")



