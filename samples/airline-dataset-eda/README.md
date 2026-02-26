# Airline Performance Dataset - EDA Sample

This directory contains a complete exploratory data analysis (EDA) example using the Databricks Airline Performance dataset. It demonstrates the "volley" workflow for interactive data exploration with Claude.

## Dataset Overview

**Source:** `databricks_airline_performance_data.v01.flights`  
**Size:** 1.24 billion records  
**Time Period:** 1987-2008 (22 years)  
**Scope:** US airline flight performance data

### Schema

| Column | Type | Description |
|--------|------|-------------|
| `ID` | Numeric | Unique record identifier |
| `Year` | Integer | Flight year |
| `FlightNum` | Integer | Flight number |
| `ArrDelay` | String/Numeric | Arrival delay in minutes (positive = delayed) |
| `UniqueCarrier` | String | 2-letter airline code |
| `TailNum` | String | Aircraft tail number |

## Directory Structure

```
airline-dataset-eda/
├── README.md                           # This file
├── docs/
│   └── ANALYSIS_REPORT.md             # Comprehensive EDA report
└── temp_code/
    ├── 02-airline_exploration.py      # Initial exploration queries
    ├── 02-airline_deep_dive.py        # Carrier & performance analysis
    └── 02-airline_insights.py         # Specific insights & trends
```

## Quick Start

### Prerequisites

1. Databricks connection configured (see main project README)
2. Authentication token refreshed
3. Access to `databricks_airline_performance_data.v01` catalog

### Running the Analysis

```bash
# From project root
cd claude-databricks-eda

# Test connection
python3 utils/token_auth_setup.py --test-connection

# Run exploration scripts
python3 samples/airline-dataset-eda/temp_code/02-airline_exploration.py
python3 samples/airline-dataset-eda/temp_code/02-airline_deep_dive.py
python3 samples/airline-dataset-eda/temp_code/02-airline_insights.py
```

## Key Findings

### Dataset Characteristics
- **1.24B records** across 22 years
- **29 unique carriers** tracked
- **13,148 aircraft** identified
- **98%+ data completeness** in most years

### Performance Insights
- **Average delay:** 6-10 minutes across decades
- **Best decade:** 1990s (6.77 min average delay)
- **Worst decade:** 2000s (7.17 min average delay)
- **Top performer:** Southwest (42.56% delay rate)
- **Most flights:** Delta (162.6M flights)

### Data Quality Notes
- `ArrDelay` stored as string, contains 'NA' values (2.09%)
- Early years (1987-1994) have 367M records with 'NA' TailNum
- Use `TRY_CAST(ArrDelay AS DOUBLE)` for numerical analysis

## Analysis Workflow

This sample demonstrates the "volley" approach:

1. **Initial Exploration** - Understanding structure, size, and basic statistics
2. **Deep Dive** - Carrier analysis, year-over-year trends, utilization metrics
3. **Specific Insights** - Targeted queries for interesting patterns
4. **Documentation** - Comprehensive report of findings

## Example Queries

### Basic Row Count
```sql
SELECT COUNT(*) as total_rows
FROM databricks_airline_performance_data.v01.flights
```

### Carrier Performance
```sql
SELECT
    UniqueCarrier,
    COUNT(*) as total_flights,
    ROUND(AVG(TRY_CAST(ArrDelay AS DOUBLE)), 2) as avg_delay
FROM databricks_airline_performance_data.v01.flights
WHERE ArrDelay != 'NA'
GROUP BY UniqueCarrier
ORDER BY total_flights DESC
```

### Year-over-Year Trends
```sql
SELECT
    Year,
    COUNT(*) as total_flights,
    ROUND(AVG(TRY_CAST(ArrDelay AS DOUBLE)), 2) as avg_delay
FROM databricks_airline_performance_data.v01.flights
WHERE ArrDelay != 'NA'
GROUP BY Year
ORDER BY Year
```

## Table Versions

The dataset is available in three optimized versions:

| Table | Optimization | Best For |
|-------|--------------|----------|
| `flights` | Z-Ordered by FlightNum | Flight number queries |
| `flights_cluster_id` | Clustered by ID | ID-based lookups |
| `flights_cluster_id_flightnum` | Clustered by ID & FlightNum | Combined queries |

All versions contain identical data (1.24B rows each).

## Performance Tips

1. **Always filter 'NA'** in delay queries: `WHERE ArrDelay != 'NA'`
2. **Use TRY_CAST** to handle string-to-numeric conversion safely
3. **Sample first** for exploratory queries: `LIMIT 1000000`
4. **Choose the right table** based on your primary query pattern
5. **Filter by Year** to reduce scan size when possible

## Data Cleaning Template

```sql
-- Create a clean view for analysis
CREATE VIEW flights_clean AS
SELECT
    ID,
    Year,
    FlightNum,
    TRY_CAST(ArrDelay AS DOUBLE) as ArrDelay,
    UniqueCarrier,
    TailNum
FROM databricks_airline_performance_data.v01.flights
WHERE ArrDelay != 'NA'
  AND TRY_CAST(ArrDelay AS DOUBLE) IS NOT NULL
  AND Year IS NOT NULL;
```

## Use Cases

This dataset is ideal for:

- **Time-series analysis** - 22 years of continuous data
- **Carrier benchmarking** - Compare performance across 29 airlines
- **Delay prediction modeling** - Rich historical delay patterns
- **Operational research** - Aircraft utilization and efficiency
- **Academic coursework** - Large-scale data analytics exercises

## Limitations

- Data ends in 2008 (not current)
- No origin/destination information included
- ArrDelay stored as string requiring type conversion
- Early years have significant 'NA' values for TailNum
- US operations only (inferred from carrier codes)

## Further Analysis Ideas

1. **Seasonal patterns** - Analyze delays by month/quarter
2. **Aircraft aging** - Correlate aircraft age with delay performance
3. **Carrier market share** - Track carrier dominance over time
4. **Hub analysis** - Identify congestion patterns (requires enrichment)
5. **Predictive modeling** - Build delay prediction models
6. **Network effects** - Analyze flight number patterns and reuse

## References

- [Full Analysis Report](docs/ANALYSIS_REPORT.md)
- [Main Project Documentation](../../README.md)
- [Databricks SQL Reference](https://docs.databricks.com/sql/language-manual/index.html)

## License

This analysis sample is part of the claude-databricks-eda project.  
Dataset provided by Databricks Academy for educational purposes.