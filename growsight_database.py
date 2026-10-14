
import psycopg2


# PostgreSQL connection settings
DB_CONFIG = {
    "host": "localhost",
    "database": "growsight_warehouse",
    "user": "postgres"
}


# Get the latest temperature reading from each zone.
def get_latest_zone_temperatures():

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT ON (s.zone_id)
                    z.zone_name,
                    s.temperature_c,
                    s.reading_timestamp
                FROM public.sensor_readings AS s
                JOIN public.dim_zone AS z
                    ON s.zone_id = z.zone_id
                ORDER BY
                    s.zone_id,
                    s.reading_timestamp DESC;
            """)

            return cursor.fetchall()


# Identify the hottest greenhouse zone.
def get_hottest_zone():

    readings = get_latest_zone_temperatures()

    if not readings:
        return None

    return max(readings, key=lambda row: row[1])


# Count historical high-risk batches.
def get_high_risk_batch_count():

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM public.staging_growth
                WHERE plants_lost * 100.0
                      / NULLIF(plants_planted, 0) >= 10;
            """)

            return cursor.fetchone()[0]


# Test database functions directly.
if __name__ == "__main__":

    print("Latest Greenhouse Temperatures:")

    readings = get_latest_zone_temperatures()

    for reading in readings:
        print(reading)

    print("\nHottest Greenhouse Zone:")
    print(get_hottest_zone())

    print("\nHigh-Risk Batch Count:")
    print(get_high_risk_batch_count())