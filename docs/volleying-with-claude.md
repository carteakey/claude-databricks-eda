# Doing EDA on Databricks with Claude Code

Most AI-assisted data work falls into one of two modes: you ask a question, the AI answers. The conversation disappears and you're left with nothing reproducible.

This is a different approach. I call it **volleying**.

---

## The idea

You and Claude go back and forth on a dataset — running queries, reasoning about the results, finding gaps — until you have a clear picture. Then you say **"punch it"** and Claude compiles everything into a documented Jupyter notebook with the code, analysis, and insights. You run it, confirm it works, done.

The output is a notebook you can share, re-run, or hand off. Not a chat transcript.

---

## How it works

Claude has access to a lightweight Databricks query client:

```python
from databricks_eda import query_databricks

df = query_databricks("SELECT * FROM schema.table LIMIT 1000", "sample")
```

Read-only by design — INSERT, UPDATE, DROP and friends are blocked at the library level.

During a volley, Claude writes temp scripts, runs them, shows you the output and its reasoning, and iterates based on your feedback. When you're satisfied, one command turns the whole session into a clean notebook.

---

## The workflow

```
you:   "let's volley on the activation funnel — why did D0 drop in Q4?"
claude: [queries, shows data, reasons about gaps]
you:   "interesting — check if it's device-specific"
claude: [queries again, compares segments]
you:   "punch it"
claude: [writes 02-activation-funnel.ipynb with all code + markdown docs]
you:   [run notebook, confirm, done]
```

---

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -e .
databricks-eda-setup --refresh-token   # OAuth via browser
databricks-eda-setup --test-connection
```

Copy `CLAUDE.md` into any new project folder — it tells Claude the full workflow automatically.

---

## vs. MCP / direct tool access

The alternative is giving Claude an MCP tool that fetches data on demand. That works well for one-off questions. The difference:

| | MCP | Volleying |
|---|---|---|
| Output | Chat only | Versioned notebook |
| Code | None | Python files on disk |
| Reproducible | No | Yes |
| Best for | Quick lookups | Structured EDA |

**MCP = Claude uses your data. Volleying = Claude and you build something together.**
