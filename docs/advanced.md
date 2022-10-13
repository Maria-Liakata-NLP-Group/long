# Advanced Usage

## Accessing the JupyterLab instance

Within LoNG there is an instance of JupyterLab running. This can be reached using the URL:

```
http://localhost/jupyter/
```

## Importing external notebooks

Any files in the repo's `unmanaged` directory can be loaded into JupyterLab.

### Notes on importing local python modules

All imported code appears within Jupyter under the `/notebooks` directory. If you have code which is spread over several files and directories but is not formally packaged (eg using setup.py or pyproject.toml) then you will need to ensure that all part of your project can be imported. The `sys.path` value (which is used to locate modules for import) for a notebook will have the directory containing the notebook and a number of system-wide directories, eg:

```
['/notebooks/my_project/notebooks', '/opt/conda/lib/python310.zip', '/opt/conda/lib/python3.10', '/opt/conda/lib/python3.10/lib-dynload', '', '/opt/conda/lib/python3.10/site-packages']
```

If you need to import code relative to another directory you will need to add it to the `sys.path` before any imports in your notebook. For example, if your project is structured like so:

```
.
└── my_project
    ├── README.md
    ├── notebooks
    │   ├── explore_data.ipynb
    │   └── visualise_results.ipynb
    └── complex_processing
        ├── add.py
        └── subtract.py
```

To be able to include the statement `import complex_processing.add` in one of the notebooks, you would need to insert a code cell before the import statement:

```
import sys
from pathlib import Path

# sys.path prior to alteration
print(sys.path)

# This section will need to be adjusted to your needs and project structure
#
# Include a check to ensure that the path does get inserted multiple time if the
# code cell is run multiple times. Here:
# sys.path[0] is the directory containing the notebook
# sys.path[1] may or may not be parent directory. We will test for this and insert it into `sys.path` if it is not.
# We use the `resolve(strict=True)` with the strict=True parameter to ensure that the directories are are comparing are both absolute and valid.

first_path = str(Path(sys.path[0]).parent.resolve(strict=True))
second_path = str(Path(sys.path[1]).resolve(strict=True))

if first_path != second_path
    sys.path.insert(1, second_path)

# sys.path prior to alteration
print(sys.path)
```

-- END --
