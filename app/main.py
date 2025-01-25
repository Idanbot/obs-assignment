import requests
import util
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/weather/', methods=['GET'])
def get_random_weather():
    city = util.get_random_city()
    lat = city["lat"]
    lon = city["lon"]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,temperature_2m_min&past_days=45"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
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
    
@app.route('/health/', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
