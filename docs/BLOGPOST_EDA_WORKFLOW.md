# AI-Assisted EDA on Databricks: The Volleying Workflow

**TL;DR:** Perform exploratory data analysis on Databricks by "volleying" with AI agents like Claude or Copilot—iterate quickly with SQL queries, get insights in real-time, and generate polished notebooks automatically.

## The Problem

Exploratory Data Analysis (EDA) on large-scale data platforms like Databricks is typically slow and manual:
- Writing SQL queries, running them, interpreting results
- Context-switching between IDE, notebooks, and data platform
- Documenting findings as you go
- Converting exploration scripts into shareable notebooks

What if your AI coding assistant could handle the heavy lifting?

## The Solution: Volleying Workflow

This template enables a collaborative "volleying" workflow where you and your AI agent iterate on data exploration together:

**You**: "Let's explore the airline performance dataset"  
**AI**: *Queries Databricks, shows results, provides insights*  
**You**: "Dig deeper into carrier delays"  
**AI**: *Refines analysis, shares new findings*  
**You**: "Punch it!" (finalize)  
**AI**: *Generates complete notebook with code + documentation*

## How It Works

### 1. Setup (One-Time)

```bash
# Clone and configure
git clone https://github.com/carteakey/claude-databricks-eda.git my-analysis
cd my-analysis

# Add your Databricks credentials to .env
cp .env.template .env

# Install dependencies
uv venv && source .venv/bin/activate && uv sync

# Test connection
python3 utils/token_auth_setup.py --test-connection
```

### 2. Start Volleying

Tell your AI agent to "volley" on a dataset. The agent will:

1. **Query Databricks** using the secure `databricks_query.py` client
2. **Save temp code** to `notebooks/temp_code/XX-topic.py`
3. **Show results** as pandas DataFrames with reasoning
4. **Iterate** based on your feedback

Example:
```python
from utils.databricks_query import query_databricks

df = query_databricks("""
    SELECT UniqueCarrier, 
           COUNT(*) as flights,
           ROUND(AVG(TRY_CAST(ArrDelay AS DOUBLE)), 2) as avg_delay
    FROM databricks_airline_performance_data.v01.flights
    WHERE ArrDelay != 'NA'
    GROUP BY UniqueCarrier
    ORDER BY flights DESC
""", query_name="Carrier Performance")
```

The AI interprets results, suggests next steps, and helps you explore patterns.

### 3. Finalize ("Punch It")

When satisfied, tell the agent to "punch it." It will:

1. Review all volleying iterations
2. Consolidate temp code files
3. Generate `notebooks/XX-topic.ipynb` with:
   - Executable code blocks
   - Markdown documentation
   - Analysis insights
4. Validate with `jupytext` QA checks

### 4. Verify and Share

Execute the notebook to confirm everything works. You now have:
- **Reproducible analysis** in a clean notebook
- **Documented insights** from the volleying process
- **Production-ready code** tested during exploration

## Key Features

**🔒 Secure by Design**
- SQL injection protection (blocks INSERT/UPDATE/DELETE/DROP)
- Supports only read operations: SELECT, SHOW, DESCRIBE, WITH (CTEs)
- Automatic credential management

**⚡ Fast Iteration**
- Direct Databricks SQL execution via REST API
- Results as pandas DataFrames for immediate analysis
- No context-switching between tools

**📊 AI-Powered Insights**
- Agent interprets data patterns
- Suggests next exploration steps
- Documents findings automatically

**✅ Quality Assurance**
- Built-in jupytext validation
- Automatic path handling for scripts vs notebooks
- Data type conversion helpers

## Real-World Example

Check out `samples/airline-dataset-eda/` for a complete example analyzing 1.24B flight records:

**Initial Query:**
```sql
SELECT Year, COUNT(*) as flights
FROM databricks_airline_performance_data.v01.flights
GROUP BY Year ORDER BY Year
```

**AI Insight:** "22 years of data (1987-2008), relatively consistent volume except peak in mid-2000s."

**Follow-Up:** "Which carriers had the best on-time performance?"

**AI Response:** *Runs carrier analysis, identifies Southwest as top performer with 42.56% on-time rate, provides comparison table*

After 5-10 volleys, you have a comprehensive EDA notebook documenting the entire journey.

## Best Practices

1. **Start broad, then narrow**: Overview queries → specific patterns
2. **Let the AI explain**: Ask "what does this data tell us?"
3. **Iterate quickly**: Don't perfect each query—iterate and refine
4. **Trust the QA**: The agent validates notebooks before finalizing
5. **Use temp_code freely**: Experimentation is cheap, documentation happens at the end

## When to Use This Workflow

**✅ Perfect For:**
- Initial data exploration and profiling
- Ad-hoc analysis questions
- Learning new datasets
- Generating shareable analysis notebooks

**❌ Not Ideal For:**
- Production ETL pipelines
- Data modification operations
- Real-time dashboards

## Technical Details

**Architecture:**
```
You ←→ AI Agent ←→ databricks_query.py ←→ Databricks SQL REST API
         ↓
    temp_code/*.py (iteration)
         ↓
    notebooks/*.ipynb (final)
```

**Supported SQL:**
- `SELECT` queries (with JOINs, subqueries, CTEs)
- `SHOW TABLES`, `SHOW COLUMNS`
- `DESCRIBE` / `DESC` table
- `WITH` clauses (Common Table Expressions)

**Blocked Operations:**
- INSERT, UPDATE, DELETE
- DROP, CREATE, ALTER
- TRUNCATE, GRANT, REVOKE

## Getting Started

1. **Clone the repo**: `git clone https://github.com/carteakey/claude-databricks-eda.git`
2. **Read the docs**: `QUICKSTART.md` and `AGENTS.md`
3. **Try the sample**: Run `samples/airline-dataset-eda/` scripts
4. **Start volleying**: Point your AI agent to a dataset and explore

## Conclusion

The volleying workflow transforms EDA from a solo, manual process into an interactive collaboration with AI. By combining:
- Secure Databricks access
- Fast SQL iteration
- AI-powered insights
- Automatic documentation

You can explore data faster, with better documentation, and more confidence.

**Ready to try it?** Clone the repo and start volleying.

---

**Project**: [carteakey/claude-databricks-eda](https://github.com/carteakey/claude-databricks-eda)  
**Author**: Akshay Karthik  
**License**: MIT (inferred)
