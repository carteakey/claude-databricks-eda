#!/usr/bin/env python3
"""
Temporary exploration code for airline performance dataset
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
    print("Airline Performance Dataset - Initial Exploration")
    print("=" * 80)

    # Initialize client
    try:
        client = DatabricksQueryClient(debug=False)
        print("✅ Connected to Databricks")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return

    # 1. Basic table info - row count and structure
    print("\n1. Verifying table structure and row count...")
    query = """
    SELECT COUNT(*) as total_rows
    FROM databricks_airline_performance_data.v01.flights
    """
    result = client.execute_query(query, "Row Count")
    total = int(result["total_rows"].iloc[0])
    print(f"\nTotal rows: {total:,}")

    # 2. Sample rows to understand the data
    print("\n2. Sample data (5 rows)...")
    query = """
    SELECT *
    FROM databricks_airline_performance_data.v01.flights
    LIMIT 5
    """
    result = client.execute_query(query, "Sample Data")
    print(result.to_string(index=False))

    # 3. Year range
    print("\n3. Year range in dataset...")
    query = """
    SELECT
        MIN(Year) as earliest_year,
        MAX(Year) as latest_year,
        COUNT(DISTINCT Year) as total_years
    FROM databricks_airline_performance_data.v01.flights
    """
    result = client.execute_query(query, "Year Range")
    print(result.to_string(index=False))

    # 4. Carrier information
    print("\n4. Number of unique carriers...")
    query = """
    SELECT
        COUNT(DISTINCT UniqueCarrier) as total_carriers
    FROM databricks_airline_performance_data.v01.flights
    """
    result = client.execute_query(query, "Carrier Count")
    print(result.to_string(index=False))

    # 5. Flight delay summary statistics
    print("\n5. Arrival delay statistics...")
    query = """
    SELECT
        COUNT(*) as total_flights,
        COUNT(ArrDelay) as flights_with_delay_data,
        COUNT(TRY_CAST(ArrDelay AS DOUBLE)) as flights_with_numeric_delay,
        AVG(TRY_CAST(ArrDelay AS DOUBLE)) as avg_delay_minutes,
        MIN(TRY_CAST(ArrDelay AS DOUBLE)) as min_delay,
        MAX(TRY_CAST(ArrDelay AS DOUBLE)) as max_delay,
        PERCENTILE(TRY_CAST(ArrDelay AS DOUBLE), 0.5) as median_delay
    FROM databricks_airline_performance_data.v01.flights
    """
    result = client.execute_query(query, "Delay Stats")
    print(result.to_string(index=False))

    # 5b. Check for non-numeric values in ArrDelay
    print("\n5b. Non-numeric values in ArrDelay...")
    query = """
    SELECT
        ArrDelay,
        COUNT(*) as occurrences
    FROM databricks_airline_performance_data.v01.flights
    WHERE TRY_CAST(ArrDelay AS DOUBLE) IS NULL AND ArrDelay IS NOT NULL
    GROUP BY ArrDelay
    ORDER BY occurrences DESC
    LIMIT 10
    """
    result = client.execute_query(query, "Non-numeric Delays")
    print(result.to_string(index=False))

    # 6. Check for NULL values in sample
    print("\n6. NULL value analysis (1M row sample)...")
    query = """
    SELECT
        COUNT(*) as total_rows,
        SUM(CASE WHEN ID IS NULL THEN 1 ELSE 0 END) as null_id,
        SUM(CASE WHEN Year IS NULL THEN 1 ELSE 0 END) as null_year,
        SUM(CASE WHEN FlightNum IS NULL THEN 1 ELSE 0 END) as null_flightnum,
        SUM(CASE WHEN ArrDelay IS NULL THEN 1 ELSE 0 END) as null_arrdelay,
        SUM(CASE WHEN UniqueCarrier IS NULL THEN 1 ELSE 0 END) as null_carrier,
        SUM(CASE WHEN TailNum IS NULL THEN 1 ELSE 0 END) as null_tailnum
    FROM databricks_airline_performance_data.v01.flights
    LIMIT 1000000
    """
    result = client.execute_query(query, "NULL Analysis")
    print(result.to_string(index=False))

    print("\n" + "=" * 80)
    print("Initial exploration complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
