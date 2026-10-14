import psycopg2
import random
import time
from datetime import datetime

conn = psycopg2.connect(
    host="localhost",
    database="growsight_warehouse",
    user="postgres",

)

cursor = conn.cursor()

zone_targets = {
    1: 24.0,
    2: 27.0,
    3: 23.0
}

zone_temperatures = {
    1: 24.0,   # North Glasshouse
    2: 27.0,   # South Tunnel
    3: 23.0    # Propagation Room
}

while True:
    zone_id = random.choice([1, 2, 3])

    target = zone_targets[zone_id]
    current = zone_temperatures[zone_id]

    drift = random.uniform(-0.2, 0.2)
    pull_to_normal = (target - current) * 0.1

    zone_temperatures[zone_id] += drift + pull_to_normal

    sensor_reading = {
        "timestamp": datetime.now(),
        "zone_id": zone_id,
        "temperature_c": round(zone_temperatures[zone_id], 1),
        "humidity_percent": round(random.uniform(45, 80), 1),
        "ph_level": round(random.uniform(5.5, 6.8), 2),
        "ec_level": round(random.uniform(1.5, 3.2), 2)
    }

    print(sensor_reading)

    cursor.execute(
        """
        INSERT INTO public.sensor_readings (
            reading_timestamp,
            zone_id,
            temperature_c,
            humidity_percent,
            ph_level,
            ec_level
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            sensor_reading["timestamp"],
            sensor_reading["zone_id"],
            sensor_reading["temperature_c"],
            sensor_reading["humidity_percent"],
            sensor_reading["ph_level"],
            sensor_reading["ec_level"]
        )
    )

    conn.commit()

    time.sleep(5)