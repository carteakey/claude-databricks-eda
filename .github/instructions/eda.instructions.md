---
applyTo: '**'
---
# Volleying with Claude Code for Data Analytics EDA

## approach
- when I say "volley" I want claude code to use the tools in databricks_eda/ to run queries in databricks, look at the returned data, try to understand it, including any gaps in what we thought it would have returned, reason with it and show me the output and its reasoning
- Before starting refresh the token by running token auth setup with refresh-token param.

```
databricks-eda-setup --refresh-token
# or: python -m databricks_eda.token_auth_setup --refresh-token
```

- Test connection and then start. No alarms and no surprises.
```
databricks-eda-setup --test-connection
# or: python -m databricks_eda.token_auth_setup --test-connection
```
- Copilot can put this temp code in notebooks/temp_code/[0-9]{2}
-<filename>.py files where the first two digits match the notebook prefix we will be working on
- Sample code is present in temp_code directory to make things easier  (01-initial_dataset_exploration.py)
- i would then ask it to try a few things based on the data returned and it would write more temp code..
- We will go back and forth until I tell it to "punch it"
- at this command,
    - it would look back at our back and forth,
    - look at the temp code files and then
    - write up or update the [0-9]{2}-<filename>.ipynb complete with
        - the code blocks
        - followed by markdown text blocks
        - which document the progressive code and analysis that was performed during the volleying and
        - the insights gained from the reasoning
    - when done with the notebook, it would return back to me
- I would execute the notebook and confirm all is working and this would be the end of the specific EDA cycle

- Sample
```python
from databricks_eda import DatabricksQueryClient, query_databricks
```


## quality assurance step
- after creating the notebook, Copilot should use jupytext to convert it to .py format and run the .py version to check for errors
- common issues to fix:
    - **path issues**: since `databricks_eda` is installed as a package (`pip install -e .`), use `from databricks_eda import ...` directly — no `sys.path` manipulation needed in either `.py` scripts or `.ipynb` notebooks
    - **data type issues**: pandas DataFrames from Databricks may return object/string types, use `pd.to_numeric()` for calculations
    - **import issues**: ensure all required libraries are properly imported
- **CRITICAL**: since the package is installed, both `.py` and `.ipynb` files use the same import style
- **VERIFY ALL CELLS**: check the entire notebook for ANY remaining `sys.path` hacks or `__file__` path manipulations — they should not be needed

## common jupytext issues to watch for
- **duplicate cells**: jupytext conversion may create multiple import cells, remove duplicates
- **markdown cells with code**: code accidentally placed in markdown cells instead of code cells
- **always validate**: run `grep` commands to verify no stale `sys.path` or `__file__` references remain in the final notebook
