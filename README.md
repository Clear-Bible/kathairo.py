# Getting Started
1. Clone this Repository
2. Install Python 3.11 (not 3.12).  When you install Python 3.11 make sure to add it to your `PATH` variable to make it easier to run from the command-line
3. Open the command-line
4. Navigate into the kathairo.py repo
5. Run `pip install poetry` to install the Python dependency management system that kathario uses
6. Run `poetry shell` to enter the Poetry command-line (no worries if this fails though, just continue in the regular shell)
7. Run `poetry install` to install all of kathairo's dependencies 

# To Build All Target TSVs
1. Add a project's details to `kathairo\Prompts\prompts.json`.
2. In the `\kathairo.py` directory, run `python kathairo\build_tsv_wrapper.py` to construct TSVs for all projects in `prompts.json`

# To Build/Debug a Specific Target TSV
Either:
- Temporarily remove unwanted prompts from `prompts.json`
- Add/Uncomment appropriate project details to `build_tsv.py`

# To Run Unit Tests
All target TSVs specified in `prompts.json` will be tested when the unit tests are run.

On the command-line, in `\kathairo.py`, run `pytest -n auto`.  

Add `-s` to the end if you want to see the output of the optional tests.  

For a specific test, run `pytest test/<FILE_NAME>::<TEST_NAME> -n auto`.  
For example, to run the test_source_chapter_size test you'd enter `pytest test/test_tsv_optional.py::test_source_chapter_size`.

# Versification Tests
After running `pytest -n auto`, the `versification_issues` directory will be updated.  There are four ways versification is tested:
1. Source Mappings - Looking at the `source_verse` column, are all the source-verses present which are listed in the mappings section of the target versification?
2. Source Size - Looking at the `source_verse` column, are the number of verses in each chapter the same as the chapter sizes defined by `org.vrs`?
3. Target Mappings - Looking at the `id` column, are all the target-verses present which are listed in the mappings section of the target versification?
4. Target Size - Looking at the `id` column, are the number of verses in each chapter the same as the chapter sizes defined by the target versification?

Modifying the target versification file, whether the chapter size or mappings section, is how to fix any of the above issues.

# Before Committing to Main
1. Undo any temporary changes made to `prompts.json` 
2. Add new project details to `prompts.json`
3. Run `build_tsv_wrapper.py`
4. Run `pytest -n auto`
5. Version any modified word-level/verse-level TSVs 

# Resources Provenance
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

IRVAsm - USFM
    https://open.bible/bibles/assamese-bridge-text-bible

IRVBen - USFM
    https://open.bible/bibles/bengali-bridge-text-bible/

IRVHin - USFM
    https://app.thedigitalbiblelibrary.org/entry/download_listing?id=1e8ab327edbce67f&license=26429&revision=

RUSSYN - USFM
    from Sean / Dima at TextTree
    https://git.door43.org/Door43-Catalog/ru_rsb
    
Auxillary Russian Texts:
    russyn_USFM
        https://ebible.org/details.php?id=russyn

    syno_uld_ru
        https://door43.org/u/STR/ru_rsb/bfb6f3be9e/

ONEN - USFM
    https://open.bible/bibles/swahili-biblica-text-bible/

ONEN - USX
    https://open.bible/bibles/swahili-biblica-text-bible/

ONEN2024 (not included) - USFM
    from Pieter

ONEN2024 (not included) - USX
    from Pieter

JFA11 - USFM
    https://github.com/Clear-Bible/internal-Alignments/tree/main/data/JFA11/usfm

RV09 - USX
    https://app.thedigitalbiblelibrary.org/entry?id=592420522e16049f

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
