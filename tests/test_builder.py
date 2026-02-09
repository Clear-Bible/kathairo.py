import pytest
import os
import shutil
from pathlib import Path


def test_builder_fluent_api():
    """Test fluent builder API creates TSV files correctly."""
    import kathairo

    test_output_dir = "test_builder_output"
    test_data_dir = Path(__file__).parent.parent.parent / "kathairo-data"

    # Clean up if exists
    if os.path.exists(test_output_dir):
        shutil.rmtree(test_output_dir)

    try:
        # Use fluent builder API
        kathairo.from_usfm_corpus(str(test_data_dir / "resources/arb/arb-vd_usfm")) \
            .with_versification(str(test_data_dir / "resources/arb/arb-vd_usfm/versification.vrs")) \
            .with_project_name("AVD") \
            .with_output_dir(test_output_dir) \
            .use_latin_ws_tokenizer() \
            .build()

        # Verify files were created
        token_file = os.path.join(test_output_dir, "token", "token_AVD.tsv")
        verse_file = os.path.join(test_output_dir, "verse", "verse_AVD.tsv")

        assert os.path.exists(token_file), f"Token file not found at {token_file}"
        assert os.path.exists(verse_file), f"Verse file not found at {verse_file}"

        # Verify files have content
        assert os.path.getsize(token_file) > 0, "Token file is empty"
        assert os.path.getsize(verse_file) > 0, "Verse file is empty"

    finally:
        # Clean up
        if os.path.exists(test_output_dir):
            shutil.rmtree(test_output_dir)


def test_builder_from_usx_corpus():
    """Test builder works with USX corpus."""
    import kathairo

    test_output_dir = "test_usx_output"
    test_data_dir = Path(__file__).parent.parent.parent / "kathairo-data"

    if os.path.exists(test_output_dir):
        shutil.rmtree(test_output_dir)

    try:
        # Find a USX corpus in test data
        usx_path = test_data_dir / "resources/arb/onav_usx/release/USX_1"
        if not usx_path.exists():
            pytest.skip("USX test data not available")

        kathairo.from_usx_corpus(str(usx_path)) \
            .with_versification(str(test_data_dir / "resources/arb/onav_usx/release/versification.vrs")) \
            .with_project_name("ONAV") \
            .with_output_dir(test_output_dir) \
            .use_latin_ws_tokenizer() \
            .build()

        # Verify files were created
        assert os.path.exists(os.path.join(test_output_dir, "token", "token_ONAV.tsv"))
        assert os.path.exists(os.path.join(test_output_dir, "verse", "verse_ONAV.tsv"))

    finally:
        if os.path.exists(test_output_dir):
            shutil.rmtree(test_output_dir)


def test_builder_chaining():
    """Test that builder methods can be chained in any order."""
    import kathairo

    test_output_dir = "test_chain_output"
    test_data_dir = Path(__file__).parent.parent.parent / "kathairo-data"

    if os.path.exists(test_output_dir):
        shutil.rmtree(test_output_dir)

    try:
        # Chain in different order
        kathairo.from_usfm_corpus(str(test_data_dir / "resources/arb/arb-vd_usfm")) \
            .use_latin_ws_tokenizer() \
            .exclude_cross_references() \
            .with_project_name("AVD") \
            .with_versification(str(test_data_dir / "resources/arb/arb-vd_usfm/versification.vrs")) \
            .with_output_dir(test_output_dir) \
            .build()

        # Verify files exist
        assert os.path.exists(os.path.join(test_output_dir, "token", "token_AVD.tsv"))

    finally:
        if os.path.exists(test_output_dir):
            shutil.rmtree(test_output_dir)
