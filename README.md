# kathairo

### Scripture Processing Library: Parse, Tokenize, and Versify

[![PyPI version](https://badge.fury.io/py/kathairo.svg)](https://badge.fury.io/py/kathairo)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**kathairo** is a comprehensive Python library for Scripture text processing that converts USFM and USX formats into structured TSV files. Built on [SIL's machine.py](https://github.com/sillsdev/machine.py), kathairo provides both verse-level and token-level outputs.

## Quick Start

```bash
pip install kathairo
```

```python
import kathairo

# Simple fluent API
kathairo.from_usfm_corpus("path/to/usfm") \
    .with_project_name("MyBible") \
    .with_versification("path/to/versification.vrs") \
    .with_language("eng") \
    .use_latin_ws_tokenizer() \
    .build()

# Output: output/eng/MyBible/token/token_MyBible.tsv
#         output/eng/MyBible/verse/verse_MyBible.tsv
```

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Fluent Builder API](#fluent-builder-api)
  - [Function API](#function-api)
  - [Config File API](#config-file-api)
- [Output Format](#output-format)
- [Configuration Options](#configuration-options)
- [Examples](#examples)
- [Testing](#testing)
- [Contributing](#contributing)
- [API Reference](#api-reference)

## Installation

### Requirements

- Python 3.11 or 3.12
- Dependencies (automatically installed):
  - `sil-machine==1.8.4`
  - `spacy>=3.7.5`
  - `polars>=1.4.0`
  - `pandas>=3.0.0`

### Install from PyPI

```bash
pip install kathairo
```

### Install for Development

```bash
git clone https://github.com/Clear-Bible/kathairo.py.git
cd kathairo.py
poetry install
```

## Usage

kathairo offers three APIs to fit your workflow:

### Fluent Builder API

The builder pattern provides method chaining:

```python
import kathairo

# Start with a corpus source
kathairo.from_usfm_corpus("resources/eng/ESV/usfm") \
    .with_project_name("ESV") \
    .with_versification("resources/eng/versification.vrs") \
    .with_language("eng") \
    .use_latin_ws_tokenizer() \
    .exclude_cross_references() \
    .build()
```

**Type Safety:** The builder enforces required parameters at development time. Your IDE won't show `.build()` until you've provided:
- A corpus source (from\_usfm\_corpus, from\_usx\_corpus, or from\_tsv)
- A project name (`.with_project_name()`)
- An output location (`.with_language()` or `.with_output_dir()`)

### Function API

```python
import kathairo

kathairo.create_tsv(
    targetUsfmCorpusPath="resources/eng/ESV/usfm",
    projectName="ESV",
    targetVersificationPath="resources/eng/versification.vrs",
    language="eng",
    latinWhiteSpaceIncludedTokenizer=True,
    excludeCrossReferences=True
)
```

### Config File API

**projects.json:**
```json
[
  {
    "projectName": "ESV",
    "language": "eng",
    "targetUsfmCorpusPath": "resources/eng/ESV/usfm",
    "targetVersificationPath": "resources/eng/versification.vrs",
    "latinWhiteSpaceIncludedTokenizer": true,
    "excludeCrossReferences": true
  },
  {
    "projectName": "RVR1960",
    "language": "spa",
    "targetUsfmCorpusPath": "resources/spa/RVR1960/usfm",
    "targetVersificationPath": "resources/spa/versification.vrs",
    "latinWhiteSpaceIncludedTokenizer": true
  }
]
```

**Process in parallel:**
```python
import kathairo

kathairo.from_config_file("projects.json").build()
```

## Output Format

### Default Output Structure

```
output/
└── {language}/
    └── {projectName}/
        ├── token/
        │   └── token_{projectName}.tsv
        └── verse/
            └── verse_{projectName}.tsv
```

### Custom Output Directory

```python
kathairo.from_usfm_corpus("path/to/usfm") \
    .with_project_name("MyBible") \
    .with_versification("path/to/versification.vrs") \
    .with_output_dir("custom/output/path") \
    .use_latin_ws_tokenizer() \
    .build()

# Output: custom/output/path/token/token_MyBible.tsv
#         custom/output/path/verse/verse_MyBible.tsv
```

### Verse-Level TSV

| Column                   | Description                        |
| ------------------------ | ---------------------------------- |
| `id`                     | Verse identifier (BBCCCVVV format) |
| `source_verse`           | Source versification verse ID      |
| `text`                   | Complete verse text                |
| `id_range_end`           | End verse for verse ranges         |
| `source_verse_range_end` | End verse in source versification  |

### Token-Level TSV

| Column                   | Description                                      |
| ------------------------ | ------------------------------------------------ |
| `id`                     | Token identifier (BBCCCVVVWWW format)            |
| `source_verse`           | Source versification verse ID                    |
| `text`                   | Token text                                       |
| `skip_space_after`       | "y" if no space should follow, empty otherwise   |
| `exclude`                | "y" if token should be excluded, empty otherwise |
| `id_range_end`           | End verse for verse ranges                       |
| `source_verse_range_end` | End verse in source versification                |
| `required`               | "y" if token contains non-punctuation            |

**Example Token Output (Genesis 1:1):**
```tsv
id           source_verse  text       skip_space_after  exclude  required
01001001001  01001001      In                                    y
01001001002  01001001      the                                   y
01001001003  01001001      beginning                             y
01001001004  01001001      God                                   y
01001001010  01001001      earth      y                          y
01001001011  01001001      .                            y        n
```

## Configuration Options

### Required Parameters

| Parameter                       | Description                                       |
| ------------------------------- | ------------------------------------------------- |
| `projectName`                   | Project identifier (used in file naming)          |
| **One corpus source:**          |                                                   |
| `targetUsfmCorpusPath`          | Path to USFM files directory                      |
| `targetUsxCorpusPath`           | Path to USX files directory                       |
| `tsvPath`                       | Path to existing token TSV (for re-versification) |
| **One output location:**        |                                                   |
| `language`                      | Language code (creates output/{language}/{projectName}/) |
| `output_dir`                    | Custom output directory                           |
| **One tokenizer:**              |                                                   |
| `latinTokenizer`                | Standard Latin word tokenizer                     |
| `latinWhiteSpaceIncludedTokenizer` | Latin tokenizer with whitespace preservation (recommended) |
| `chineseTokenizer`              | Chinese Bible word tokenizer                      |

### Optional Parameters

| Parameter                      | Type    | Description                                  |
| ------------------------------ | ------- | -------------------------------------------- |
| `targetVersificationPath`      | string  | Path to versification file (.vrs). Defaults to English versification if not provided. |
| `treatApostropheAsSingleQuote` | boolean | Handle apostrophes as single quotes          |
| `excludeBracketedText`         | boolean | Exclude text within square brackets          |
| `excludeCrossReferences`       | boolean | Exclude cross-reference text                 |
| `stopWordsPath`                | string  | Path to TSV file containing stop words       |
| `zwRemovalPath`                | string  | Path to TSV file for zero-width char removal |
| `regexRulesPath`               | string  | Path to custom regex rules module            |
| `psalmSuperscriptionTag`       | string  | USFM tag for psalm superscriptions (default: "d") |

## Examples

### Example 1: Basic USFM Processing

```python
import kathairo

kathairo.from_usfm_corpus("resources/eng/ESV/usfm") \
    .with_project_name("ESV") \
    .with_versification("resources/eng/versification.vrs") \
    .with_language("eng") \
    .use_latin_ws_tokenizer() \
    .build()
```

### Example 2: Custom Output Directory

```python
kathairo.from_usfm_corpus("path/to/usfm") \
    .with_project_name("MyBible") \
    .with_versification("path/to/versification.vrs") \
    .with_output_dir("~/Documents/bible-data") \
    .use_latin_ws_tokenizer() \
    .build()
```

### Example 3: USX with Exclusions

```python
kathairo.from_usx_corpus("resources/eng/NIV/usx") \
    .with_project_name("NIV") \
    .with_versification("resources/eng/versification.vrs") \
    .with_language("eng") \
    .use_latin_ws_tokenizer() \
    .exclude_cross_references() \
    .exclude_bracketed_text() \
    .build()
```

### Example 4: Chinese Scripture

```python
kathairo.from_usfm_corpus("resources/zho/CUV/usfm") \
    .with_project_name("CUV") \
    .with_versification("resources/zho/versification.vrs") \
    .with_language("zho") \
    .use_chinese_tokenizer() \
    .build()
```

### Example 5: With Stop Words and Custom Rules

```python
kathairo.from_usfm_corpus("resources/hin/IRV/usfm") \
    .with_project_name("IRVHin") \
    .with_versification("resources/hin/versification.vrs") \
    .with_language("hin") \
    .use_latin_ws_tokenizer() \
    .with_stop_words("resources/hin/stopwords.tsv") \
    .with_zw_removal("resources/hin/zw_removal.tsv") \
    .with_regex_rules("resources/hin/custom_regex.py") \
    .exclude_cross_references() \
    .build()
```

### Example 6: Re-versification

```python
# Re-versify an existing token TSV with a new versification
kathairo.from_tsv("output/eng/ESV/token/token_ESV.tsv") \
    .with_project_name("ESV_NewVersification") \
    .with_versification("resources/eng/new_versification.vrs") \
    .with_language("eng") \
    .use_latin_ws_tokenizer() \
    .build()
```

### Example 7: Multiple Projects (Function API)

```python
import kathairo

projects = [
    {
        "targetUsfmCorpusPath": "resources/eng/ESV/usfm",
        "projectName": "ESV",
        "targetVersificationPath": "resources/eng/versification.vrs",
        "language": "eng",
        "latinWhiteSpaceIncludedTokenizer": True
    },
    {
        "targetUsfmCorpusPath": "resources/spa/RVR1960/usfm",
        "projectName": "RVR1960",
        "targetVersificationPath": "resources/spa/versification.vrs",
        "language": "spa",
        "latinWhiteSpaceIncludedTokenizer": True
    }
]

for project in projects:
    kathairo.create_tsv(config_object=project)
```

## Testing

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_builder.py

# Run with verbose output
poetry run pytest -v

# Run with coverage
poetry run pytest --cov=kathairo
```

### Test Structure

- `tests/test_builder.py` - Tests for fluent builder API
- `tests/test_type_safety.py` - Tests for type-safe builder pattern
- `tests/test_output_dir.py` - Tests for output_dir functionality

## API Reference

### Builder API

```python
# Start with a corpus source
kathairo.from_usfm_corpus(path: str) -> CorpusBuilder
kathairo.from_usx_corpus(path: str) -> CorpusBuilder
kathairo.from_tsv(path: str) -> CorpusBuilder
kathairo.from_config_file(path: str) -> ConfigBuilder
kathairo.from_config(obj: dict) -> ConfigBuilder

# CorpusBuilder methods (requires .with_project_name() next)
.with_versification(path: str) -> CorpusBuilder
.use_latin_tokenizer() -> CorpusBuilder
.use_latin_ws_tokenizer() -> CorpusBuilder
.use_chinese_tokenizer() -> CorpusBuilder
.exclude_bracketed_text() -> CorpusBuilder
.exclude_cross_references() -> CorpusBuilder
.treat_apostrophe_as_single_quote() -> CorpusBuilder
.with_psalm_superscription_tag(tag: str) -> CorpusBuilder
.with_regex_rules(path: str) -> CorpusBuilder
.with_stop_words(path: str) -> CorpusBuilder
.with_zw_removal(path: str) -> CorpusBuilder
.with_metadata_source_url(url: str) -> CorpusBuilder
.with_metadata_path(path: str) -> CorpusBuilder
.with_metadata_kind(kind: str) -> CorpusBuilder
.with_project_name(name: str) -> ProjectBuilder

# ProjectBuilder methods (requires .with_language() or .with_output_dir() next)
# ... same configuration methods as CorpusBuilder
.with_language(lang: str) -> CompleteBuilder
.with_output_dir(path: str) -> CompleteBuilder

# CompleteBuilder methods (can call .build())
# ... same configuration methods
.build() -> None
```

### Function API

```python
kathairo.create_tsv(
    # Config sources (use one)
    config_path: str = None,
    config_object: dict = None,

    # Direct parameters
    targetUsfmCorpusPath: str = None,
    targetUsxCorpusPath: str = None,
    tsvPath: str = None,
    targetVersificationPath: str = None,
    latinTokenizer: bool = False,
    latinWhiteSpaceIncludedTokenizer: bool = False,
    chineseTokenizer: bool = False,
    excludeBracketedText: bool = False,
    excludeCrossReferences: bool = False,
    psalmSuperscriptionTag: str = 'd',
    treatApostropheAsSingleQuote: bool = False,
    regexRulesPath: str = None,
    stopWordsPath: str = None,
    zwRemovalPath: str = None,
    language: str = None,
    projectName: str = None,
    output_dir: str = None,
    metadata_source_url: str = None,
    metadata_path: str = None,
    metadata_kind: str = None
) -> None
```

## Project Structure

```
kathairo/
├── src/kathairo/
│   ├── parsing/          # USFM and USX parsers
│   ├── tokenization/     # Tokenizer implementations
│   ├── tsvs/            # TSV building and processing
│   ├── versification/   # Versification utilities
│   ├── helpers/         # Utility functions
│   ├── params.py        # Parameter definitions (source of truth)
│   ├── api.py           # Main API (create_tsv function)
│   └── builder.py       # Fluent builder pattern
├── tests/               # Test suite
│   ├── test_builder.py
│   ├── test_output_dir.py
│   └── test_type_safety.py
└── pyproject.toml
```

## Author

**Robertson Brinker** - [robertson.brinker@biblica.com](mailto:robertson.brinker@biblica.com)

## Acknowledgments

- Built on [SIL's machine.py](https://github.com/sillsdev/machine.py) - Machine learning and NLP library for Scripture
- Type-safe builder pattern inspired by modern API design principles

---

## For Maintainers

### Publishing to PyPI

1. Update version in `pyproject.toml`
2. Run tests: `poetry run pytest`
3. Build and publish:
```bash
poetry config repositories.pypi https://upload.pypi.org/legacy/
poetry publish --build --username __token__ --password <api-token>
```
