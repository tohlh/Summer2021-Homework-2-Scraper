import psycopg2
from psycopg2 import Error
import SECRETS

connection = psycopg2.connect(user = SECRETS.db_username,
                              password = SECRETS.db_password,
                              host = SECRETS.db_address,
                              port = SECRETS.db_port,
                              database = SECRETS.db_name)

def connectDB():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record)

    except (Exception, Error) as error:
        print('Unable to connect to database')