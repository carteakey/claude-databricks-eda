# Databricks EDA Template with Claude Code

A template for doing Databricks EDA with Claude using the "volleying" workflow.

## Quick Start

```bash
# 1. Clone
git clone <repo-url>
cd claude-databricks-eda-v2

# 2. Setup environment
cp .env.template .env
# Edit .env with your Databricks credentials

# 3. Install dependencies
uv venv && source .venv/bin/activate && uv sync
# Or: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# 4. Configure Databricks CLI (if needed)
export DATABRICKS_CLI_DO_NOT_EXECUTE_NEWER_VERSION=1
./.venv/bin/databricks configure --oauth --host https://${DATABRICKS_SERVER_HOSTNAME}

# 5. Refresh token and test
echo "sql" | python3 utils/token_auth_setup.py --refresh-token
python3 utils/token_auth_setup.py --test-connection
```

## The Volleying Workflow

1. **You ask**: "Let's volley on [dataset] to understand [question]"
2. **Claude writes**: Code in `notebooks/temp_code/XX-topic.py`
3. **Claude queries**: Databricks and shows results + reasoning
4. **Iterate**: Back and forth until satisfied
5. **You say**: "Punch it" 
6. **Claude creates**: Final notebook `notebooks/XX-topic.ipynb` with all code + docs
7. **You verify**: Run the notebook

See [AGENTS.md](AGENTS.md) for details.

## Project Structure

```
.
├── .env                    # Your credentials (DO NOT COMMIT)
├── CHANGELOG.md            # Version history
├── AGENTS.md               # Volley workflow guide
├── utils/
│   ├── databricks_query.py # Query client
│   └── token_auth_setup.py # Token management
├── notebooks/
│   ├── temp_code/          # Volleying code goes here
│   └── *.ipynb            # Final notebooks
├── samples/
│   └── airline-dataset-eda/  # Example analysis (1.24B records)
└── docs/
    └── TODO.md
```

## Using the Query Client

```python
from databricks_query import DatabricksQueryClient

client = DatabricksQueryClient(debug=False)
df = client.execute_query("""
    SELECT manufacturer, COUNT(*) as count
    FROM my_table
    WHERE date >= '2025-08-01'
    GROUP BY manufacturer
""", "Manufacturer Count")

print(df)
```

**Supported SQL**: SELECT, SHOW, DESCRIBE/DESC, WITH (CTEs)  
**Blocked**: INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, TRUNCATE

## Key Features

- ✅ SQL injection protection
- ✅ Automatic .env loading
- ✅ Returns pandas DataFrames
- ✅ Supports DESCRIBE and WITH clauses
- ✅ Volleying workflow with Claude
- ✅ Jupytext QA validation

## Common Issues

**Path errors in notebooks:**
```python
# For .py scripts:
sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))

# For .ipynb notebooks:
sys.path.insert(0, str(Path.cwd().parent / 'utils'))
```

**Token expired:**
```bash
echo "sql" | python3 utils/token_auth_setup.py --refresh-token
```

**Data type issues:**
```python
df['col'] = pd.to_numeric(df['col'], errors='coerce')
```

## Sample Analysis

See `samples/airline-dataset-eda/` for a complete example:
- 1.24B flight records (1987-2008)
- Full EDA with comprehensive report
- Demonstrates volley workflow

## Using as a Template

```bash
git clone <this-repo> my-new-project
cd my-new-project
rm -rf .git && git init
cp .env.template .env
# Edit .env, then: uv sync
```

---

**That's it. Clone, setup .env, start volleying with Claude.**# claude-databricks-eda
