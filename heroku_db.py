import os
import psycopg2


def connect_heroku_db():
    DATABASE_URL = os.getenv("HEROKU_DATABASE_URL")
    connection = psycopg2.connect(DATABASE_URL, sslmode="require")
    cursor = connection.cursor()
    
    # Creates SQL table to store data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_results (
            id SERIAL PRIMARY KEY,
            search_id TEXT UNIQUE,
            keyword TEXT,
            results JSONB
        )
    """)

    connection.commit()
    return connection, cursor
