import os
import json
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "weatherdb"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password")
}

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def is_city_in_db(city_name):
    query = "SELECT EXISTS (SELECT 1 FROM cities WHERE city_name = %s)"
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (city_name,))
                return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error checking database for city: {e}")
        return False

def add_city(city_name, latitude, longitude):
    query = "INSERT INTO cities (city_name, latitude, longitude) VALUES (%s, %s, %s) ON CONFLICT (city_name) DO NOTHING"
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (city_name, latitude, longitude))
                conn.commit()
                print(f"City {city_name} added to database.")
                return True
    except Exception as e:
        print(f"Error adding city to database: {e}")
        return False

def get_city_id(city_name):
    query = "SELECT id FROM cities WHERE city_name = %s"
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (city_name,))
                result = cursor.fetchone()
                return result[0] if result else None
    except Exception as e:
        print(f"Error fetching city ID: {e}")
        return None

def add_weather_data(city_id, date, weather_data):
    query = "INSERT INTO weather_data (city_id, date, weather_data) VALUES (%s, %s, %s)"
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (city_id, date, json.dumps(weather_data)))
                conn.commit()
                print(f"Weather data for city ID {city_id} on {date} added to database.")
                return True
    except Exception as e:
        print(f"Error adding weather data to database: {e}")
        return False
    
def add_weather_data_bulk(city_id, weather_data_list):
    query = "INSERT INTO weather_data (city_id, date, weather_data) VALUES %s"
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                values = [(city_id, day["dt"], json.dumps(day))for day in weather_data_list]
                execute_values(cursor, query, values)
                conn.commit()
                print(f"Inserted {len(weather_data_list)} weather records for city ID {city_id}.")
                return True
    except Exception as e:
        print(f"Error adding bulk weather data to database: {e}")
        return False

def get_weather_data(city_name):
    query = """
    SELECT w.date, w.weather_data 
    FROM weather_data w 
    JOIN cities c ON w.city_id = c.id 
    WHERE c.city_name = %s
    ORDER BY w.date
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (city_name.strip(),))
                print(f"Fetching weather data for {city_name}")
                return cursor.fetchall()
    except Exception as e:
        return None

def fetch_last_30_days_weather(city_name):
    query = """
    SELECT w.weather_data
    FROM weather_data w
    JOIN cities c ON w.city_id = c.id
    WHERE c.city_name ILIKE %s AND w.date >= (CURRENT_DATE - INTERVAL '30 days')
    ORDER BY w.date
    LIMIT 31
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (city_name.strip(),))
                rows = cursor.fetchall()
                return rows
    except Exception as e:
        print(f"Error fetching last 30 days weather data for {city_name}: {e}")
        return None
