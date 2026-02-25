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

# 4. Authenticate with Databricks
# Install Go-based Databricks CLI if needed: brew install databricks/tap/databricks
databricks-eda-setup --refresh-token   # opens browser for OAuth
databricks-eda-setup --test-connection # verify
```

## The Volleying Workflow

1. **You ask**: "Let's volley on [dataset] to understand [question]"
2. **Claude writes**: Code in `notebooks/temp_code/XX-topic.py`
3. **Claude queries**: Databricks and shows results + reasoning
4. **Iterate**: Back and forth until satisfied
5. **You say**: "Punch it" 
6. **Claude creates**: Final notebook `notebooks/XX-topic.ipynb` with all code + docs
7. **You verify**: Run the notebook

See [docs/eda-volleying-with-claude.md](docs/eda-volleying-with-claude.md) for details.

## Project Structure

```
.
├── .env                    # Your credentials (DO NOT COMMIT)
├── pyproject.toml          # uv dependencies
├── requirements.txt        # pip fallback
├── databricks_eda/
│   ├── databricks_query.py # Query client (supports SELECT, SHOW, DESCRIBE, WITH)
│   └── token_auth_setup.py # Token management (also: databricks-eda-setup CLI)
├── notebooks/
│   ├── temp_code/          # Volleying code goes here
│   └── *.ipynb            # Final notebooks
└── docs/
    └── eda-volleying-with-claude.md  # Workflow guide
```

## Using the Query Client

```python
from databricks_eda import query_databricks

df = query_databricks("""
    SELECT manufacturer, COUNT(*) as count
    FROM my_table
    WHERE date >= '2025-08-01'
    GROUP BY manufacturer
""", query_name="Manufacturer Count")

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

**Token expired:**
```bash
databricks-eda-setup --refresh-token
```

**Data type issues:**
```python
df['col'] = pd.to_numeric(df['col'], errors='coerce')
```

## Starting a New EDA Project

This repo acts as a shared library. New projects install from it — they don't copy the code.

```bash
# 1. Create your project folder
mkdir my-new-eda && cd my-new-eda

# 2. Set up credentials
cp ~/repos/eda/claude-databricks-eda/.env.template .env
# Edit .env with your Databricks credentials

# 3. Set up venv and install the package
uv venv && source .venv/bin/activate
uv pip install -e ~/repos/eda/claude-databricks-eda

# 4. Authenticate
databricks-eda-setup --refresh-token
databricks-eda-setup --test-connection

# 5. Copy the Claude instructions and scaffold notebooks
cp ~/repos/eda/claude-databricks-eda/CLAUDE.md .
mkdir -p notebooks/temp_code
```

The `-e` (editable) install means any improvements to `databricks_eda` are immediately available in all your projects — no reinstall needed.

## MCP Server vs This Tool

There are two ways to give Claude access to Databricks: a local MCP server (like [`adhoc`](../adhoc)) or this EDA tool. They solve different problems.

### How the MCP approach works
The MCP server runs as a local HTTP process (`fastmcp run ... --port 5555`). Claude calls a single tool — `fetch_data(query)` — which returns CSV. Claude gets the data and reasons about it in context. You never see code written; the SQL exists only in the conversation.

### How this tool works
Claude writes actual Python files (`notebooks/temp_code/`), executes them, shows you the output and its reasoning, iterates, then compiles everything into a documented Jupyter notebook.

### Side-by-side

| | MCP Server (`adhoc`) | This EDA Tool |
|---|---|---|
| **Code visibility** | None — SQL lives in the chat | Full — Python files written to disk |
| **Reproducibility** | None — conversation disappears | Jupyter notebooks you can re-run |
| **Output** | CSV string returned to Claude | pandas DataFrames + saved notebooks |
| **SQL safety** | Any SQL, including writes | Read-only enforced (SELECT/SHOW/DESCRIBE) |
| **Connection** | SQLAlchemy pool (persistent process) | REST API per-query (no server to manage) |
| **Setup overhead** | Run a server, register with Claude | Just `uv sync` + `.env` |
| **Token refresh** | Manual | `databricks-eda-setup --refresh-token` |

### When to use the MCP server
- Quick one-off questions: "how many rows in this table?", "what columns does X have?"
- Conversational data lookup during normal work
- You want Claude to pull data as part of a broader task (writing a doc, answering a question)
- You don't need to keep the analysis

### When to use this tool
- You're doing a structured EDA that will produce a deliverable
- You want the queries and code to be visible, editable, and version-controlled
- You need a reproducible notebook someone else can run
- You're iterating deeply on a dataset and want to track your reasoning
- The analysis matters enough to document

### The short version
**MCP = Claude uses data. This tool = Claude and you build something together.**

---

**That's it. Clone, setup .env, start volleying with Claude.**