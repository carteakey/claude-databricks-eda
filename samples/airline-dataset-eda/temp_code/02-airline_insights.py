#!/usr/bin/env python3
"""
Temporary exploration code for airline performance dataset - Specific Insights
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
    print("Airline Performance Dataset - Specific Insights")
    print("=" * 80)

    # Initialize client
    try:
        client = DatabricksQueryClient(debug=False)
        print("✅ Connected to Databricks")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return

    # 1. Best and worst performing carriers by average delay
    print("\n1. Carriers ranked by average delay performance...")
    query = """
    SELECT
        UniqueCarrier,
        COUNT(*) as total_flights,
        ROUND(AVG(TRY_CAST(ArrDelay AS DOUBLE)), 2) as avg_delay_minutes,
        ROUND(PERCENTILE(TRY_CAST(ArrDelay AS DOUBLE), 0.5), 2) as median_delay,
        ROUND(STDDEV(TRY_CAST(ArrDelay AS DOUBLE)), 2) as stddev_delay
    FROM databricks_airline_performance_data.v01.flights
    WHERE ArrDelay != 'NA' AND TRY_CAST(ArrDelay AS DOUBLE) IS NOT NULL
    GROUP BY UniqueCarrier
    HAVING COUNT(*) > 1000000
    ORDER BY avg_delay_minutes ASC
    """
    result = client.execute_query(query, "Carrier Rankings")
    print(result.to_string(index=False))

    # 2. Performance trends over time - Are flights getting better or worse?
    print("\n2. Decade-level performance trends...")
    query = """
    SELECT
        CASE
            WHEN Year BETWEEN 1987 AND 1989 THEN '1987-1989'
            WHEN Year BETWEEN 1990 AND 1999 THEN '1990s'
            WHEN Year BETWEEN 2000 AND 2008 THEN '2000s'
        END as decade,
        COUNT(*) as total_flights,
        ROUND(AVG(TRY_CAST(ArrDelay AS DOUBLE)), 2) as avg_delay,
        COUNT(CASE WHEN TRY_CAST(ArrDelay AS DOUBLE) > 15 THEN 1 END) as flights_delayed_15plus,
        ROUND(COUNT(CASE WHEN TRY_CAST(ArrDelay AS DOUBLE) > 15 THEN 1 END) * 100.0 / COUNT(*), 2) as pct_delayed_15plus
    FROM databricks_airline_performance_data.v01.flights
    WHERE ArrDelay != 'NA' AND Year IS NOT NULL
    GROUP BY decade
    ORDER BY decade
    """
    result = client.execute_query(query, "Decade Trends")
    print(result.to_string(index=False))

    # 3. Sample of extreme delays
    print("\n3. Examples of extreme delays (>300 minutes)...")
    query = """
    SELECT
        Year,
        UniqueCarrier,
        FlightNum,
        TailNum,
        TRY_CAST(ArrDelay AS DOUBLE) as delay_minutes
    FROM databricks_airline_performance_data.v01.flights
    WHERE TRY_CAST(ArrDelay AS DOUBLE) > 300
    ORDER BY delay_minutes DESC
    LIMIT 10
    """
    result = client.execute_query(query, "Extreme Delays")
    print(result.to_string(index=False))

    # 4. Comparison of the three table versions (basic structure check)
    print("\n4. Comparing table versions - row counts...")
    queries = [
        (
            "flights",
            "SELECT COUNT(*) as count FROM databricks_airline_performance_data.v01.flights",
        ),
        (
            "flights_cluster_id",
            "SELECT COUNT(*) as count FROM databricks_airline_performance_data.v01.flights_cluster_id",
        ),
        (
            "flights_cluster_id_flightnum",
            "SELECT COUNT(*) as count FROM databricks_airline_performance_data.v01.flights_cluster_id_flightnum",
        ),
    ]

    for table_name, query in queries:
        try:
            result = client.execute_query(query, f"Count {table_name}")
            count = int(result["count"].iloc[0])
            print(f"  {table_name}: {count:,} rows")
        except Exception as e:
            print(f"  {table_name}: Error - {e}")

    # 5. Year with most complete data
    print("\n5. Data completeness by year...")
    query = """
    SELECT
        Year,
        COUNT(*) as total_records,
        COUNT(CASE WHEN ArrDelay != 'NA' AND TRY_CAST(ArrDelay AS DOUBLE) IS NOT NULL THEN 1 END) as complete_delay_data,
        ROUND(COUNT(CASE WHEN ArrDelay != 'NA' AND TRY_CAST(ArrDelay AS DOUBLE) IS NOT NULL THEN 1 END) * 100.0 / COUNT(*), 2) as pct_complete
    FROM databricks_airline_performance_data.v01.flights
    WHERE Year IS NOT NULL
    GROUP BY Year
    ORDER BY Year DESC
    """
    result = client.execute_query(query, "Data Completeness")
    print(result.to_string(index=False))

    # 6. Most frequent flight numbers
    print("\n6. Top 10 most frequent flight numbers...")
    query = """
    SELECT
        FlightNum,
        COUNT(*) as occurrences,
        COUNT(DISTINCT UniqueCarrier) as num_carriers,
        COUNT(DISTINCT Year) as years_active,
        ROUND(AVG(TRY_CAST(ArrDelay AS DOUBLE)), 2) as avg_delay
    FROM databricks_airline_performance_data.v01.flights
    WHERE FlightNum IS NOT NULL AND ArrDelay != 'NA'
    GROUP BY FlightNum
    ORDER BY occurrences DESC
    LIMIT 10
    """
    result = client.execute_query(query, "Top Flight Numbers")
    print(result.to_string(index=False))

    # 7. Understanding the ID column distribution
    print("\n7. ID column characteristics...")
    query = """
    SELECT
        MIN(ID) as min_id,
        MAX(ID) as max_id,
        COUNT(DISTINCT ID) as unique_ids,
        COUNT(*) as total_records
    FROM databricks_airline_performance_data.v01.flights
    """
    result = client.execute_query(query, "ID Analysis")
    print(result.to_string(index=False))

    print("\n" + "=" * 80)
    print("Insights analysis complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
