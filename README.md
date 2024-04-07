# Getting Started
1. Clone this Repository
2. Install Python 3.11 (not 3.12).  When you install Python make sure to add it to your PATH variable to make it easier to run fomr the commandline
3. Open the commandline
4. Navigate into the kathairo.py repo
5. Run `pip install poetry` to install the Python dependency management system kathario uses
6. Run `poetry shell` to enter the Poetry commandline (no worries if this fails though)
7. Run `poetry install` to install all of kathairo's dependencies 

# To Build All TSVs
1. Add a project's details to `prompts.json`.
2. Change the method at the bottom of `build_tsv_args_parser.py` to be either word-level or verse-level
3. In the `\kathairo.py` repo, run `python kathairo/build_tsv_wrapper.py` to construct TSVs for each file in `prompts.json`

# To Build One TSV
Either:
- Move all unwanted prompts into `prompts_unused.json`
- Uncomment/Add appropriate project details to `build_tsv.py`

# Run Unit Tests
On the command-line, in `\kathairo.py`, run `py.test.exe`.  Use `py.test.exe -n <NUM>` to run tests in parallel.  Alternatively, run `py.test.exe -s` if you want to see the output of the optional tests.

# WIP
- USFM/USX validation