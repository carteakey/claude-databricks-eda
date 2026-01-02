#!/usr/bin/env python3
"""
01 - Initial Dataset Exploration Template
==========================================

This script provides a template for initial exploration of any Databricks dataset.
Replace the table_name and customize queries as needed for your specific dataset.

Template demonstrates:
- Connection testing
- Basic row count and structure
- Sample data preview
- Column statistics
- NULL value analysis
- Data quality assessment
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
    """Explore the dataset structure and basic statistics."""

    print("=" * 80)
    print("Initial Dataset Exploration")
    print("=" * 80)

    # Initialize client
    try:
        client = DatabricksQueryClient(debug=False)
        print("✅ Connected to Databricks")
    except Exception as e:
        print(f"❌ Failed to connect to Databricks: {e}")
        return

    # TODO: Replace with your table name
    table_name = "catalog_name.schema_name.table_name"

    print(f"\n📊 Exploring table: {table_name}")
    print("-" * 80)

    # 1. Get basic row count
    print("\n1️⃣ Getting row count...")
    query = f"""
    SELECT COUNT(*) as total_rows
    FROM {table_name}
    """

    try:
        result = client.execute_query(query, "Row Count")
        total = int(result["total_rows"].iloc[0])
        print(f"   Total rows: {total:,}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    # 2. Get table schema by examining first row
    print("\n2️⃣ Getting table schema...")
    query = f"""
    SELECT *
    FROM {table_name}
    LIMIT 1
    """

    try:
        first_row = client.execute_query(query, "Schema Check")
        print(f"   Table has {len(first_row.columns)} columns")
        print("\n   Column Names:")
        for i, col in enumerate(first_row.columns, 1):
            dtype = first_row[col].dtype
            print(f"     {i:2d}. {col:<30} ({dtype})")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    # 3. Sample data preview
    print("\n3️⃣ Sample data preview...")
    query = f"""
    SELECT *
    FROM {table_name}
    LIMIT 5
    """

    try:
        sample = client.execute_query(query, "Sample Data")
        print(f"\n   First 5 rows (showing first 5 columns):")
        cols_to_show = min(5, len(sample.columns))
        print(sample.iloc[:, :cols_to_show].to_string(index=False))
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # 4. Column-level statistics (customize based on your schema)
    print("\n4️⃣ Getting basic statistics...")
    # Example: Adjust column names as needed
    query = f"""
    SELECT
        COUNT(*) as total_records,
        COUNT(DISTINCT id) as unique_ids
        -- Add more column-specific stats here
    FROM {table_name}
    """

    try:
        stats = client.execute_query(query, "Basic Stats")
        print("\n   Dataset Statistics:")
        for col in stats.columns:
            val = stats[col].iloc[0]
            if isinstance(val, (int, float)):
                print(f"     {col}: {val:,}")
            else:
                print(f"     {col}: {val}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # 5. Check for NULL values (customize column list)
    print("\n5️⃣ NULL value analysis...")
    # Example: Replace column names with your actual columns
    query = f"""
    SELECT
        COUNT(*) as total_rows,
        SUM(CASE WHEN column1 IS NULL THEN 1 ELSE 0 END) as null_column1,
        SUM(CASE WHEN column2 IS NULL THEN 1 ELSE 0 END) as null_column2
        -- Add more columns as needed
    FROM {table_name}
    LIMIT 1000000
    """

    try:
        nulls = client.execute_query(query, "NULL Analysis")
        print("\n   NULL Value Counts (1M row sample):")
        for col in nulls.columns:
            val = nulls[col].iloc[0]
            print(f"     {col}: {val:,}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # 6. Data quality summary
    print("\n6️⃣ Data quality assessment...")
    query = f"""
    SELECT
        COUNT(*) as total_records,
        -- Add completeness checks for key columns
        ROUND(COUNT(CASE WHEN column1 IS NOT NULL THEN 1 END) * 100.0 / COUNT(*), 2) as pct_complete_column1
    FROM {table_name}
    """

    try:
        quality = client.execute_query(query, "Data Quality")
        print("\n   Data Quality Metrics:")
        print(quality.to_string(index=False))
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n" + "=" * 80)
    print("Initial exploration complete!")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Review the schema and adjust queries for your specific columns")
    print("  2. Identify key dimensions and metrics to analyze")
    print("  3. Create additional temp code files for deeper analysis")
    print("  4. Use 'volley' workflow to iterate on findings")
    print("  5. Run 'punch it' when ready to generate final notebook")


if __name__ == "__main__":
    main()
