# kathairo.py

### Parsing, Tokenizing, and Versifying Scripture.

Using SIL's machine.py, kathairo ingests USFM/USX and outputs TSV files in both verse-level and token-level formats.

`machine.py`'s parsers have been modified to include psalm-superscription (and `machine.py`'s tokenizers have been improved as well)

# How To Use (aspirationally)

### Create Verse-Level TSVs
- `kathario.create_verse_tsv_from_usfm(usfm_path, (output_path))`
- `kathario.create_verse_tsv_from_usx(usx_path, (output_path))`
- `kathario.create_verse_tsv_from_config(config_path, (output_path))`

### Create Token-Level TSVs
- `kathario.create_token_tsv_from_usfm(corpus_path, (output_path))`
- `kathario.create_token_tsv_from_usx(corpus_path, (output_path))`
- `kathario.create_token_tsv_from_config(corpus_path, (output_path))`

### (WIP) Create Versification Files
- `kathario.create_versification(config_path, (outout_path))`

### Note to self: To update python package
1. `poetry config repositories.pypi https://upload.pypi.org/legacy/`
2. `$env:PYPI_USERNAME="__token__"`
3. `$env:PYPI_PASSWORD="<api-token>"`
4. `poetry publish --build --username $env:PYPI_USERNAME --password $env:PYPI_PASSWORD`

