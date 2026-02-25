# ABOUTME: databricks_eda package — secure Databricks query client for Claude Code EDA workflows
from databricks_eda.databricks_query import (
    DatabricksQueryClient,
    query_databricks,
    test_databricks_connection,
)

__all__ = ["DatabricksQueryClient", "query_databricks", "test_databricks_connection"]
