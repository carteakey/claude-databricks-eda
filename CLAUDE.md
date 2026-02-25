# Volleying with Claude Code for Data Analytics EDA

## Guiding Principles
1. **Simplicity First**: Minimal approach. Avoid unnecessary complexity, libraries, or build tools.
2. **Conciseness**: Less noise = more focus. Keep documentation, output, and visualizations tight and purposeful.
3. **YAGNI**: The best code is no code. Don't add features not needed right now.

---

## new project setup
When starting a fresh project (no venv yet):
```bash
mkdir my-new-eda && cd my-new-eda
cp ~/repos/eda/claude-databricks-eda/.env.template .env
# edit .env with your Databricks credentials

uv venv && source .venv/bin/activate
uv pip install -e ~/repos/eda/claude-databricks-eda

databricks-eda-setup --refresh-token
databricks-eda-setup --test-connection

mkdir -p notebooks/temp_code
```
Then copy this `CLAUDE.md` into the new project root and start volleying.

The `-e` (editable) install means any updates to the `databricks_eda` package are picked up automatically across all projects.

---

## approach
- when I say "volley" I want Claude Code to use the tools in `databricks_eda/` to run queries in Databricks, look at the returned data, try to understand it, including any gaps in what we thought it would have returned, reason with it and show me the output and its reasoning
- Before starting, refresh the token:
```
databricks-eda-setup --refresh-token
# or: python -m databricks_eda.token_auth_setup --refresh-token
```
- Test connection and then start. No alarms and no surprises.
```
databricks-eda-setup --test-connection
# or: python -m databricks_eda.token_auth_setup --test-connection
```
- Temp code goes in `notebooks/temp_code/[0-9]{2}-<filename>.py` where the first two digits match the notebook prefix being worked on
- Sample code is present in `temp_code/` (e.g. `01-initial_dataset_exploration.py`)
- We go back and forth until I say **"punch it"** — at that command:
    - look back at our back and forth and the temp code files
    - write up or update `[0-9]{2}-<filename>.ipynb` with code blocks followed by markdown text blocks documenting the analysis and insights
    - return back to me when done
- I execute the notebook to confirm all is working — end of the EDA cycle

### import style
Since `databricks_eda` is installed (`pip install -e .`), use this everywhere — no `sys.path` manipulation needed:
```python
from databricks_eda import DatabricksQueryClient, query_databricks
```

### spark/local query fallback
For notebooks that run both locally and on Databricks:
```python
def run_query(query: str) -> pd.DataFrame:
    if 'spark' in globals() and spark is not None:
        return spark.sql(query).toPandas()
    from databricks_eda import query_databricks
    return query_databricks(query)
```

---

## sample query patterns

### single query (temp_code files)
```python
from databricks_eda import query_databricks

q = """
SELECT col1, col2, COUNT(*) AS cnt
FROM schema.table
WHERE condition
GROUP BY col1, col2
LIMIT 1000
"""
df = query_databricks(q, "descriptive_name")
print(df.shape)
df.head()
```

### multiple queries (reuse client)
```python
from databricks_eda import DatabricksQueryClient

client = DatabricksQueryClient()
df1 = client.execute_query(q1, "first_query")
df2 = client.execute_query(q2, "second_query")
```

### error handling
```python
try:
    df = query_databricks(q, "my_query", timeout=30)
except RuntimeError as e:
    print(f"API error: {e}")   # connection/API failure
except ValueError as e:
    print(f"Bad query: {e}")   # blocked SQL or bad credentials
```

---

## quality assurance
- use jupytext to convert the notebook to `.py` and run it to check for errors
- **data type issues**: pandas DataFrames from Databricks may return object/string types; use `pd.to_numeric()` for calculations
- **CRITICAL**: both `.py` and `.ipynb` use the same import — no `__file__` or `sys.path` hacks
- **VERIFY**: `grep -n "__file__\|sys.path" notebooks/filename.ipynb` — should return nothing

### jupytext gotchas
- **duplicate cells**: conversion may create multiple import cells — remove them
- **code in markdown cells**: check that code blocks landed in code cells, not markdown

---

## code rules
- All code files start with a 2-line comment: each line begins `ABOUTME: `
- NEVER make changes unrelated to the current task
- Match the style and formatting of surrounding code
- Names describe what, not how — no implementation details (`JSONParser`), no temporal context (`NewAPI`, `LegacyHandler`)
- Always find the **root cause** of bugs — never fix a symptom or stack multiple fixes at once

---

## jupyter notebooks
- Abstract heavy logic into classes under `src/`; tests go under `test/`
- Write the test first, then the class; import into the notebook so it works first time

---

## version control
- NEVER skip or disable a pre-commit hook
- Before committing any file, verify it has no credentials — if it does, add to `.gitignore`
- Commit messages: `type(scope): short description` (e.g. `fix(query): handle null metric rollup`)

### commit workflow
1. Update `docs/CHANGELOG.md` — new entry under today's date, SemVer, `Added`/`Changed`/`Fixed`
2. Update `docs/TODO.md` if you added or fixed something notable
3. Commit
4. Push to all remotes:
```bash
git push origin main      # work GitHub
git push personal main    # local personal repo (instant, offline)
git push carteakey main   # personal GitHub
```

---

## confidential work
- NEVER commit or push content from any folder with `confidential` (any case) in its name — stays local only
