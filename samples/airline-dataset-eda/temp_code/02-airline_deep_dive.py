#!/usr/bin/env python3
"""
Temporary exploration code for airline performance dataset - Deep Dive
Dataset: databricks_airline_performance_data.v01.flights
"""

import os
import sys
from pathlib import Path

# Add utils to path for importing - use absolute path to avoid issues
project_root = Path(__file__).parent.parent.parent
utils_path = project_root / "utils"
sys.path.insert(0, str(utils_path))

from databricks_query import DatabricksQueryClient


def main():
    print("=" * 80)
    print("Airline Performance Dataset - Deep Dive Analysis")
    print("=" * 80)

    # Initialize client
    try:
        client = DatabricksQueryClient(debug=False)
        print("✅ Connected to Databricks")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return

    # 1. Carrier performance analysis
    print("\n1. Top 10 carriers by flight volume...")
    query = """
    SELECT
        UniqueCarrier,
        COUNT(*) as total_flights,
        COUNT(CASE WHEN TRY_CAST(ArrDelay AS DOUBLE) > 0 THEN 1 END) as delayed_flights,
        ROUND(COUNT(CASE WHEN TRY_CAST(ArrDelay AS DOUBLE) > 0 THEN 1 END) * 100.0 / COUNT(*), 2) as delay_pct,
        ROUND(AVG(TRY_CAST(ArrDelay AS DOUBLE)), 2) as avg_delay_minutes
    FROM databricks_airline_performance_data.v01.flights
    WHERE ArrDelay != 'NA'
    GROUP BY UniqueCarrier
    ORDER BY total_flights DESC
    LIMIT 10
    """
    result = client.execute_query(query, "Top Carriers")
    print(result.to_string(index=False))

    # 2. Year-over-year trend
    print("\n2. Year-over-year flight volume and delay trends...")
    query = """
    SELECT
        Year,
        COUNT(*) as total_flights,
        COUNT(CASE WHEN ArrDelay != 'NA' THEN 1 END) as flights_with_delay_data,
        COUNT(CASE WHEN TRY_CAST(ArrDelay AS DOUBLE) > 0 THEN 1 END) as delayed_flights,
        ROUND(AVG(TRY_CAST(ArrDelay AS DOUBLE)), 2) as avg_delay_minutes
    FROM databricks_airline_performance_data.v01.flights
    GROUP BY Year
    ORDER BY Year
    """
    result = client.execute_query(query, "YoY Trends")
    print(result.to_string(index=False))

    # 3. Delay distribution buckets
    print("\n3. Delay distribution (for flights with numeric delays)...")
    query = """
    SELECT
        CASE
            WHEN TRY_CAST(ArrDelay AS DOUBLE) < -30 THEN 'Very Early (< -30 min)'
            WHEN TRY_CAST(ArrDelay AS DOUBLE) BETWEEN -30 AND -1 THEN 'Early (-30 to -1 min)'
            WHEN TRY_CAST(ArrDelay AS DOUBLE) BETWEEN 0 AND 15 THEN 'On Time (0-15 min)'
            WHEN TRY_CAST(ArrDelay AS DOUBLE) BETWEEN 16 AND 30 THEN 'Minor Delay (16-30 min)'
            WHEN TRY_CAST(ArrDelay AS DOUBLE) BETWEEN 31 AND 60 THEN 'Moderate Delay (31-60 min)'
            WHEN TRY_CAST(ArrDelay AS DOUBLE) BETWEEN 61 AND 120 THEN 'Major Delay (61-120 min)'
            WHEN TRY_CAST(ArrDelay AS DOUBLE) > 120 THEN 'Severe Delay (> 120 min)'
        END as delay_category,
        COUNT(*) as flight_count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
    FROM databricks_airline_performance_data.v01.flights
    WHERE ArrDelay != 'NA' AND TRY_CAST(ArrDelay AS DOUBLE) IS NOT NULL
    GROUP BY delay_category
    ORDER BY
        CASE delay_category
            WHEN 'Very Early (< -30 min)' THEN 1
            WHEN 'Early (-30 to -1 min)' THEN 2
            WHEN 'On Time (0-15 min)' THEN 3
            WHEN 'Minor Delay (16-30 min)' THEN 4
            WHEN 'Moderate Delay (31-60 min)' THEN 5
            WHEN 'Major Delay (61-120 min)' THEN 6
            WHEN 'Severe Delay (> 120 min)' THEN 7
        END
    """
    result = client.execute_query(query, "Delay Distribution")
    print(result.to_string(index=False))

    # 4. Aircraft (TailNum) analysis
    print("\n4. Aircraft utilization insights...")
    query = """
    SELECT
        COUNT(DISTINCT TailNum) as unique_aircraft,
        AVG(flights_per_aircraft) as avg_flights_per_aircraft,
        MAX(flights_per_aircraft) as max_flights_per_aircraft,
        MIN(flights_per_aircraft) as min_flights_per_aircraft
    FROM (
        SELECT TailNum, COUNT(*) as flights_per_aircraft
        FROM databricks_airline_performance_data.v01.flights
        WHERE TailNum IS NOT NULL
        GROUP BY TailNum
    )
    """
    result = client.execute_query(query, "Aircraft Stats")
    print(result.to_string(index=False))

    # 5. Most utilized aircraft
    print("\n5. Top 10 most utilized aircraft...")
    query = """
    SELECT
        TailNum,
        COUNT(*) as total_flights,
        COUNT(DISTINCT UniqueCarrier) as carriers_operated,
        MIN(Year) as first_year,
        MAX(Year) as last_year,
        ROUND(AVG(TRY_CAST(ArrDelay AS DOUBLE)), 2) as avg_delay
    FROM databricks_airline_performance_data.v01.flights
    WHERE TailNum IS NOT NULL AND ArrDelay != 'NA'
    GROUP BY TailNum
    ORDER BY total_flights DESC
    LIMIT 10
    """
    result = client.execute_query(query, "Top Aircraft")
    print(result.to_string(index=False))

    # 6. Flight number patterns
    print("\n6. Flight number statistics...")
    query = """
    SELECT
        COUNT(DISTINCT FlightNum) as unique_flight_numbers,
        AVG(flights_per_number) as avg_flights_per_number,
        MAX(flights_per_number) as max_flights_per_number
    FROM (
        SELECT FlightNum, COUNT(*) as flights_per_number
        FROM databricks_airline_performance_data.v01.flights
        WHERE FlightNum IS NOT NULL
        GROUP BY FlightNum
    )
    """
    result = client.execute_query(query, "FlightNum Stats")
    print(result.to_string(index=False))

    # 7. Data quality summary
    print("\n7. Data quality summary...")
    query = """
    SELECT
        COUNT(*) as total_records,
        ROUND(COUNT(CASE WHEN ArrDelay = 'NA' THEN 1 END) * 100.0 / COUNT(*), 2) as pct_na_delays,
        ROUND(COUNT(CASE WHEN TailNum IS NULL THEN 1 END) * 100.0 / COUNT(*), 2) as pct_null_tailnum,
        ROUND(COUNT(CASE WHEN FlightNum IS NULL THEN 1 END) * 100.0 / COUNT(*), 2) as pct_null_flightnum,
        ROUND(COUNT(CASE WHEN UniqueCarrier IS NULL THEN 1 END) * 100.0 / COUNT(*), 2) as pct_null_carrier
    FROM databricks_airline_performance_data.v01.flights
    """
    result = client.execute_query(query, "Data Quality")
    print(result.to_string(index=False))

    print("\n" + "=" * 80)
    print("Deep dive analysis complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
