# Quick Start Guide

## Clone and Setup

```bash
# Clone to your desired directory name
git clone https://github.com/kchauhan_mcafee/databricks-eda-template.git my-eda-project
cd my-eda-project

# Disconnect from template repo and start fresh
rm -rf .git
git init
git add -A
git commit -m "Initial commit from databricks-eda-template"

# Setup environment file
cp .env.template .env
# Edit .env with your Databricks credentials:
#   DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
#   DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
#   DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/<warehouse-id>
#   DATABRICKS_ACCESS_TOKEN=<your-token>

# Install dependencies and the package (choose one)
# Option 1: Using uv (recommended)
uv venv && source .venv/bin/activate && uv sync

# Option 2: Using pip
python -m venv .venv && source .venv/bin/activate && pip install -e .

# Authenticate with Databricks (installs Go CLI once, then re-use)
# Install the new Go-based Databricks CLI if not already present:
#   brew install databricks/tap/databricks
databricks-eda-setup --refresh-token   # opens browser for OAuth
databricks-eda-setup --test-connection # verify it works
```

## Start Volleying

```
You: "Let's volley on [dataset] to understand [question]"

Claude: [writes notebooks/temp_code/01-analysis.py, queries Databricks, shows results]

You: "Dig deeper into [specific finding]"

Claude: [iterates with more analysis]

You: "Punch it!"

Claude: [creates notebooks/01-analysis.ipynb with all code + docs]
```

## What You Get

- **`databricks_eda/databricks_query.py`** - Secure query client (SELECT, SHOW, DESCRIBE, WITH)
- **`databricks_eda/token_auth_setup.py`** - Token management (also available as `databricks-eda-setup`)
- **Volleying workflow** - Iterative EDA with Claude
- **Auto QA** - Jupytext validation built-in

## Importing in Scripts and Notebooks

```python
# Clean import — no sys.path manipulation needed
from databricks_eda import query_databricks, DatabricksQueryClient

df = query_databricks("SELECT * FROM my_table LIMIT 10")
```

That's it. See [README.md](README.md) for more details.
