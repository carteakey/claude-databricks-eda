Lets explore this dataset
databricks_airline_performance_data.v01.flights

Overview
This dataset contains detailed information on airline flight performance, spanning several years, and includes metrics such as flight delays, carrier identifiers, and aircraft details. There are over 1.2 billion rows (1,235,347,780), covering multiple years of flight data.

The same data is available in three optimized versions to meet the needs of various types of queries and performance analysis (primarily for academic purposes):

    flights (Z-Ordered by FlightNum)
    flights_cluster_id (Clustered by ID)
    flights_cluster_id_flightnum (Clustered by ID and FlightNum)

Columns (Across All Versions):

    ID: Unique ID for each row
    Year: The year the flight took place.
    FlightNum: The flight number.
    ArrDelay: The arrival delay in minutes (positive values indicate delayed flights).
    UniqueCarrier: The airline carrier code.
    TailNum: The aircraft’s tail number, representing the individual plane.

There is also a smaller table included that provides a subset of the data for benchmarking purposes.

Use cases
This data is primarily for use by Databricks Academy to support course delivery.
