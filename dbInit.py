import psycopg2
from psycopg2 import Error
import SECRETS

connection = psycopg2.connect(user = SECRETS.db_username,
                              password = SECRETS.db_password,
                              host = SECRETS.db_address,
                              port = SECRETS.db_port,
                              database = SECRETS.db_name)

cursor = connection.cursor()

def connectDB():
    try:
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record)
        return True

    except (Exception, Error) as error:
        print('Unable to connect to database')
        return False

def createTables():
    create_table_query = '''CREATE TABLE videos
        (id TEXT PRIMARY KEY NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        videoThumbnail TEXT NOT NULL,
        interactionCount INT8 NOT NULL,
        likeCount INT8 NOT NULL,
        dislikeCount INT8 NOT NULL,
        uploadDate TIMESTAMPTZ NOT NULL,
        datePublished TIMESTAMP NOT NULL,
        channelID TEXT NOT NULL,
        genre TEXT NOT NULL,
        comments TEXT []); '''
    cursor.execute(create_table_query)

    create_table_query = '''CREATE TABLE channels
        (id TEXT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        profilePic TEXT NOT NULL,
        description TEXT NOT NULL,
        joinedDate TIMESTAMP NOT NULL,
        totalViews INT8 NOT NULL,
        subscriberCount TEXT NOT NULL,
        videos TEXT []); '''
    cursor.execute(create_table_query)

    create_table_query = '''CREATE TABLE videoqueue
        (id TEXT PRIMARY KEY NOT NULL,
        scraped BOOL NOT NULL); '''
    cursor.execute(create_table_query)

    create_table_query = '''CREATE TABLE channelqueue
        (id TEXT PRIMARY KEY NOT NULL,
        scraped BOOL NOT NULL); '''
    cursor.execute(create_table_query)
    connection.commit()

    print("Tables created successfully.")

def main():
    print("Initializing DB")
    if connectDB():
        createTables()

if __name__ == "__main__":
    main()