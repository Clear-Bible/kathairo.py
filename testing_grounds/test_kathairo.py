"""
Test script for kathairo with Python 3.12 compatibility.
This script processes the BSB USFM files in testing_grounds.
"""
import os
import sys
from pathlib import Path

# Print Python version for verification
print(f"Python version: {sys.version}")
print(f"Python version info: {sys.version_info}")

# Get paths
script_dir = Path(__file__).parent
usfm_dir = script_dir / "bsb_usfm"
vrs_file = usfm_dir / "versification.vrs"

# Verify paths exist
if not usfm_dir.exists():
    print(f"ERROR: USFM directory not found: {usfm_dir}")
    sys.exit(1)

if not vrs_file.exists():
    print(f"ERROR: Versification file not found: {vrs_file}")
    print("Available files in bsb_usfm:")
    for f in sorted(usfm_dir.iterdir()):
        print(f"  - {f.name}")
    sys.exit(1)

print(f"USFM directory: {usfm_dir}")
print(f"Versification file: {vrs_file}")

# Try importing kathairo
try:
    from kathairo.tsvs.build_tsv_json_parser import process_corpus
    print("Successfully imported kathairo!")
except ImportError as e:
    print(f"ERROR importing kathairo: {e}")
    print("\nAttempting to import sil-machine to check compatibility...")
    try:
        import machine
        print(f"sil-machine imported successfully: {machine.__version__ if hasattr(machine, '__version__') else 'version unknown'}")
    except ImportError as e2:
        print(f"ERROR importing sil-machine: {e2}")
    sys.exit(1)

# Configure kathairo
config = {
    "projectName": "BSB_Test",
    "language": "eng",
    "targetUsfmCorpusPath": str(usfm_dir),
    "targetVersificationPath": str(vrs_file),
    "latinWhiteSpaceIncludedTokenizer": True,
    "excludeCrossReferences": True,
}

print("\nConfiguration:")
for key, value in config.items():
    print(f"  {key}: {value}")

# Process the corpus
print("\nProcessing corpus...")
try:
    result = process_corpus(config)
    print("Processing completed successfully!")
    print(f"\nOutput files should be at:")
    print(f"  - output/eng/BSB_Test/verse/verse_BSB_Test.tsv")
    print(f"  - output/eng/BSB_Test/token/token_BSB_Test.tsv")
except Exception as e:
    print(f"ERROR during processing: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
