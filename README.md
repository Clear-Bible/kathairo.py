# Getting Started
1. Clone this Repository
2. Install Python 3.11 (not 3.12).  When you install Python make sure to add it to your PATH variable to make it easier to run from the commandline
3. Open the commandline
4. Navigate into the kathairo.py repo
5. Run `pip install poetry` to install the Python dependency management system kathario uses
6. Run `poetry shell` to enter the Poetry commandline (no worries if this fails though)
7. Run `poetry install` to install all of kathairo's dependencies 

# To Build All TSVs
1. Add a project's details to `kathairo\Prompts\prompts.json`.
2. In the `\kathairo.py` repo, run `python kathairo\build_tsv_wrapper.py` to construct TSVs for each file in `prompts.json`

# To Build One TSV
Either:
- Move all unwanted prompts into `kathairo\Prompts\prompts_unused.json`
- Uncomment/Add appropriate project details to `build_tsv.py`

# Run Unit Tests
On the command-line, in `\kathairo.py`, run `pytest`.  

Use `pytest -n <NUM>` to run tests in parallel.  

Alternatively, run `pytest -s` if you want to see the output of the optional tests.  

To run a certain test, such as the test_source_chapter_size test, run `pytest test/test_tsv_optional.py::test_source_chapter_size`.

# Provenance
AVD - USFM
    https://ebible.org/details.php?id=arb-vd

ONAV - USX
    https://app.thedigitalbiblelibrary.org/entry/download_listing?id=b17e246951402e50&license=26904&revision=

BSB - USFM
    https://berean.bible/downloads.htm

BSB - USX
    https://app.thedigitalbiblelibrary.org/entry/download_listing?id=bba9f40183526463&license=24374&revision=

YLT - USFM
    https://ebible.org/details.php?id=engylt

LSG - USFM
    from Jonathan/Reinier

LSG - USX
    https://github.com/Clear-Bible/internal-Alignments/tree/main/data/USX/fra-LSG

OHCV (revision) - USFM
    from Pieter

OCCB-simplified - USX
    https://app.thedigitalbiblelibrary.org/entry/download_listing?id=7ea794434e9ea7ee&license=42445&revision=

IRVHin - USFM
    https://github.com/Clear-Bible/internal-Alignments/tree/main/data/IRV/clean_usfm

RSB - USFM
    from Sean / Dima at TextTree

RUSSYN - USFM
    https://ebible.org/details.php?id=russyn

SYNO - USFM
    https://door43.org/u/STR/ru_rsb/bfb6f3be9e/

ONEN - USFM
    https://open.bible/bibles/swahili-biblica-text-bible/

ONEN - USX
    https://open.bible/bibles/swahili-biblica-text-bible/

ONEN2024 (not included) - USFM
    from Pieter

ONEN2024 (not included) - USX
    from Pieter

ENG
[versification_json/examples/eng.vrs at master · ubsicap/versification_json (github.com)](https://github.com/ubsicap/versification_json/blob/master/examples/eng.vrs)

LSG
based on 
[versification_json/examples/eng.vrs at master · ubsicap/versification_json (github.com)](https://github.com/ubsicap/versification_json/blob/master/examples/eng.vrs)
and
(LSG's custom.vrs from Jonathan)

LXX
[versification_json/examples/lxx.vrs at master · ubsicap/versification_json (github.com)](https://github.com/ubsicap/versification_json/blob/master/examples/lxx.vrs)

ORG
[versification_json/examples/org.vrs at master · ubsicap/versification_json (github.com)](https://github.com/ubsicap/versification_json/blob/master/examples/org.vrs)

RSC
[versification_json/examples/rsc.vrs at master · ubsicap/versification_json (github.com)](https://github.com/ubsicap/versification_json/blob/master/examples/rsc.vrs)

RSO
[versification_json/examples/rso.vrs at master · ubsicap/versification_json (github.com)](https://github.com/ubsicap/versification_json/blob/master/examples/rso.vrs)

VERSIFICATION

VUL
[versification_json/examples/vul.vrs at master · ubsicap/versification_json (github.com)](https://github.com/ubsicap/versification_json/blob/master/examples/vul.vrs)
