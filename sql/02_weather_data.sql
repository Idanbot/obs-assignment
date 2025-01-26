CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    city_id INT NOT NULL,
    date DATE NOT NULL,
    weather_data JSONB NOT NULL,
    CONSTRAINT fk_city FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
);
