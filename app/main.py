from urllib.parse import unquote
import requests
import util
from db import get_city_id, get_weather_data, fetch_last_30_days_weather, add_weather_data_bulk, add_city, is_city_in_db
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/weather/', methods=['GET'])
def get_random_weather():
    city = util.get_random_city()
    url = (
    f"https://api.open-meteo.com/v1/forecast?&daily=weather_code,temperature_2m_max,temperature_2m_min&past_days=45&"
    f"latitude={city['lat']}&longitude={city['lon']}"
    )
    
    if not is_city_in_db(city["name"]):
        add_city(city["name"], city["lat"], city["lon"])

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        daily_data = util.get_daily_data(data)
        city_id = get_city_id(city["name"])

        add_weather_data_bulk(city_id, daily_data)

        daily_data = util.get_daily_data(data)
        weather_data = {
            "city": city["name"],
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "elapsed_ms": data["generationtime_ms"],
            "weather_daily": daily_data,
        }

        return jsonify(weather_data), 200
    else:
        return jsonify({"error": "Failed to fetch weather data"}), response.status_code

@app.route('/weather/last-30-days/<city_name>', methods=['GET'])
def get_last_30_days_weather(city_name):
    city_name = unquote(city_name)
    weather_data = fetch_last_30_days_weather(city_name)
    if weather_data:
        return jsonify({"city": city_name, "weather_data": weather_data}), 200
    else:
        return jsonify({"error": f"No weather data found for the last 30 days for city: {city_name}"}), 404
    
@app.route('/weather/<city_name>', methods=['GET'])
def get_city_weather_data(city_name):
    city_name = unquote(city_name)
    weather_data = get_weather_data(city_name)
    if weather_data:
        return jsonify({"city": city_name, "weather_data": weather_data}), 200
    else:
        return jsonify({"error": f"No weather data found for city: {city_name}"}), 404
    
@app.route('/health/', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
