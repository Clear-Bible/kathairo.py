# To Build All TSVs
1. Add a project's details to `prompts.json`.
2. Change the method at the bottom of `build_tsv_args_parser.py` to be either word-level or verse-level
3. Run `build_tsv_wrapper.py` to construct TSVs for each file in `prompts.json`

# To Build One TSV
Either:
- Move all unwanted prompts into `prompts_unused.json`
- Uncomment/Add appropriate project details to `build_tsv.py`

# Run Unit Tests
On the command-line, in `\kathairo.py`, run `py.test.exe`.  Alternatively, run `py.test.exe -s` if you want to see the output of the optional tests.

# WIP
- USFM/USX validation