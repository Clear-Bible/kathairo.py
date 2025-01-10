# kathairo.py

### Parsing, Tokenizing, and Versifying Scripture.

Using SIL's machine.py, kathairo ingests USFM/USX and output TSVs at either the verse or token level.

machine.py's parsers have been modified to:

1. include psalm-superscription

machine's tokenizers have been modified to:

1. tokenizer better

# Wish kathairo could do something else? Create an issue with your suggestion or submit a PR!

# How To Use (proposed)

kathario.create_verse_tsv_from_usfm(usfm_path, (output_path))
kathario.create_verse_tsv_from_usx(usx_path, (output_path))
kathario.create_verse_tsv_from_config(config_path, (output_path))

and for these too...
kathario.create_token_tsv(corpus_path, (output_path))
kathario.create_versification(config_path, (outout_path))

1. `poetry config repositories.pypi https://upload.pypi.org/legacy/`
2. `$env:PYPI_USERNAME="__token__"`
3. `$env:PYPI_PASSWORD="<api-token>"`
4. `poetry publish --build --username $env:PYPI_USERNAME --password $env:PYPI_PASSWORD`
