import pytest
import os
import shutil
from pathlib import Path


def test_custom_output_dir():
    """Test that output_dir parameter correctly creates files in custom directory."""
    # Need to import after sys.path is set up by pytest
    import kathairo

    test_output_dir = "test_custom_output"
    test_data_dir = Path(__file__).parent.parent.parent / "kathairo-data"

    # Clean up if exists
    if os.path.exists(test_output_dir):
        shutil.rmtree(test_output_dir)

    try:
        # Test with output_dir (should NOT require language)
        kathairo.create_tsv(
            targetUsfmCorpusPath=str(test_data_dir / "resources/arb/arb-vd_usfm"),
            targetVersificationPath=str(test_data_dir / "resources/arb/arb-vd_usfm/versification.vrs"),
            projectName="AVD",
            output_dir=test_output_dir,
            latinWhiteSpaceIncludedTokenizer=True
        )

        # Check that files were created in the custom directory
        expected_token_file = os.path.join(test_output_dir, "token", "token_AVD.tsv")
        expected_verse_file = os.path.join(test_output_dir, "verse", "verse_AVD.tsv")

        assert os.path.exists(expected_token_file), f"Token file not found at {expected_token_file}"
        assert os.path.exists(expected_verse_file), f"Verse file not found at {expected_verse_file}"

        # Verify files have content
        assert os.path.getsize(expected_token_file) > 0, "Token file is empty"
        assert os.path.getsize(expected_verse_file) > 0, "Verse file is empty"

    finally:
        # Clean up
        if os.path.exists(test_output_dir):
            shutil.rmtree(test_output_dir)


def test_output_dir_creates_subdirectories():
    """Test that output_dir creates proper token/ and verse/ subdirectories."""
    import kathairo

    test_output_dir = "test_output_structure"
    test_data_dir = Path(__file__).parent.parent.parent / "kathairo-data"

    if os.path.exists(test_output_dir):
        shutil.rmtree(test_output_dir)

    try:
        kathairo.create_tsv(
            targetUsfmCorpusPath=str(test_data_dir / "resources/arb/arb-vd_usfm"),
            targetVersificationPath=str(test_data_dir / "resources/arb/arb-vd_usfm/versification.vrs"),
            projectName="TEST",
            output_dir=test_output_dir,
            latinWhiteSpaceIncludedTokenizer=True
        )

        # Verify directory structure
        assert os.path.exists(test_output_dir), "Output directory not created"
        assert os.path.exists(os.path.join(test_output_dir, "token")), "Token subdirectory not created"
        assert os.path.exists(os.path.join(test_output_dir, "verse")), "Verse subdirectory not created"

    finally:
        if os.path.exists(test_output_dir):
            shutil.rmtree(test_output_dir)
