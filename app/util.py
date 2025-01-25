import random

def get_daily_data(data):
    daily_data = data["daily"]
    return [
        {
            "dt": date,
            "temp_min": min_temp,
            "temp_max": max_temp,
            "temp_avg": (min_temp + max_temp) / 2,
            "weather_description": translate_weather_code(weather_code)
        }
        for date, min_temp, max_temp, weather_code in zip(
            daily_data["time"],
            daily_data["temperature_2m_min"],
            daily_data["temperature_2m_max"],
            daily_data["weather_code"]
        )
    ]

def translate_weather_code(code):
    range_map = {
        range(0, 1): "Clear sky",
        range(1, 4): "Mainly clear, partly cloudy, and overcast",
        range(45, 49): "Fog and depositing rime fog",
        range(51, 56): "Drizzle: Light, moderate, and dense intensity",
        range(56, 58): "Freezing Drizzle: Light and dense intensity",
        range(61, 66): "Rain: Slight, moderate and heavy intensity",
        range(66, 68): "Freezing Rain: Light and heavy intensity",
        range(71, 76): "Snow fall: Slight, moderate, and heavy intensity",
        range(77, 78): "Snow grains",
        range(80, 83): "Rain showers: Slight, moderate, and violent",
        range(85, 87): "Snow showers: Slight and heavy",
        range(95, 96): "Thunderstorm: Slight or moderate",
        range(96, 100): "Thunderstorm with slight and heavy hail"
    }

    for key_range, description in range_map.items():
        if code in key_range:
            return description

    return "Unknown weather condition"

def get_random_city():
    cities = [
        {"name": "New York", "lat": 40.7128, "lon": -74.0060},
        {"name": "London", "lat": 51.5074, "lon": -0.1278},
        {"name": "Tokyo", "lat": 35.6895, "lon": 139.6917},
        {"name": "Sydney", "lat": -33.8688, "lon": 151.2093},
        {"name": "Tel Aviv", "lat": 32.0809, "lon": 34.7806},
        {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
        {"name": "Berlin", "lat": 52.5200, "lon": 13.4050},
        {"name": "Dubai", "lat": 25.276987, "lon": 55.296249},
        {"name": "Moscow", "lat": 55.7558, "lon": 37.6173},
        {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
        {"name": "Beijing", "lat": 39.9042, "lon": 116.4074},
        {"name": "Cape Town", "lat": -33.9249, "lon": 18.4241},
        {"name": "Buenos Aires", "lat": -34.6037, "lon": -58.3816},
        {"name": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
        {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
        {"name": "Chicago", "lat": 41.8781, "lon": -87.6298},
        {"name": "Bangkok", "lat": 13.7563, "lon": 100.5018},
        {"name": "Singapore", "lat": 1.3521, "lon": 103.8198},
        {"name": "Seoul", "lat": 37.5665, "lon": 126.9780}
    ]
    return random.choice(cities)