# Volleying with Claude Code for Data Analytics EDA

**Adherence to these rules is mandatory, ALWAYS check this file and follow these rules.**

## approach
- when I say "volley" I want you to use the tools in utils/ to run queries in databricks, look at the returned data, try to understand it, including any gaps in what we thought it would have returned, reason with it and show me the output and its reasoning
- Before starting test the token connection. If it doesnt work then refresh the token by running token auth setup with refresh-token param.
- Test connection and then start. No alarms and no surprises.
```
python3 utils/token_auth_setup.py --test-connection
```
```
echo "sql" | python3 utils/token_auth_setup.py --refresh-token
```

- I want you to be less VERBOSE. More noise means less focus. Lets be more concise in all aspects especially documentation and visualizations. They need to be more concise and focused.

- you can put this temp code in notebooks/temp_code/[0-9]{2}
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
```
# Add utils to path for importing - use absolute path to avoid issues
import os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
utils_path = os.path.join(project_root, 'utils')
sys.path.insert(0, utils_path)

from databricks_query import DatabricksQueryClient, query_databricks
```


## quality assurance step
- after creating the notebook, you should use jupytext to convert it to .py format and run the .py version to check for errors
- common issues to fix:
    - **path issues for Python scripts**: use `Path(__file__).parent.parent / 'utils'` for .py files
    - **path issues for Jupyter notebooks**: use `Path.cwd().parent / 'utils'` for .ipynb files (since `__file__` is not available in notebooks)
    - **data type issues**: pandas DataFrames from Databricks may return object/string types, use `pd.to_numeric()` for calculations
    - **import issues**: ensure all required libraries are properly imported
- **CRITICAL**: after fixing errors in the .py version, manually update the notebook to use notebook-compatible paths (`Path.cwd().parent / 'utils'`)
- **VERIFY ALL CELLS**: check the entire notebook for ANY remaining `__file__` references - jupytext may create duplicate cells or leave problematic code in markdown cells
- use `grep -n "__file__" notebooks/filename.ipynb` to verify no remaining instances
- this ensures both the .py script works for testing AND the notebook works correctly when the user executes it
- **remember**: `.py` scripts need `__file__` paths, `.ipynb` notebooks need `cwd()` paths

## common jupytext issues to watch for
- **duplicate cells**: jupytext conversion may create multiple import cells, remove duplicates
- **markdown cells with code**: code accidentally placed in markdown cells instead of code cells
- **mixed path types**: some cells may still have `__file__` while others have `cwd()` - ensure consistency
- **always validate**: run `grep` commands to verify all `__file__` references are removed from the final notebook


## 📋 PRE-EDIT CHECKLIST

---
## 🧭 Guiding Principles
1. **Simplicity First**: Use a minimal approach. Avoid unnecessary complexity, libraries, or build tools.
---
## ⚠️ Prohibited Practices
---

## 🔄 Version Control & Commit Workflow
This project uses a manual versioning process. It is your responsibility to keep it accurate.
**Manual Workflow:**
1. **Code**: Make your changes following all guidelines.
2. **Test**: Thoroughly test your changes in-browser. Check for console errors and verify all functionality. 
3. **Update `docs/CHANGELOG.md`**:
  * Add a new entry under the current date.
  * Use SemVer headings and clear sections `Added`, `Changed`, `Fixed`.
```
## [1.2.3] - 2025-09-11
### Added
- video.js: keyboard shortcut “K” for pause
```
4. **Commit**: Write a short, descriptive commit message (e.g., `fix(nav): correct mobile layout overlap`).
**Pre-commit checklist:**
* Notebook tested, no console errors.
* `versions.json` bumped correctly.
* `docs/CHANGELOG.md` updated.

5. Update the docs/TODO.md file if you added or fixed something that should be noted there.
