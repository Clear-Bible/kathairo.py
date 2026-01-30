import pytest


def test_corpus_builder_has_no_build_method():
    """Test that CorpusBuilder doesn't have build() method."""
    import kathairo

    builder = kathairo.from_usfm_corpus("path/to/corpus")

    assert type(builder).__name__ == "CorpusBuilder"
    assert not hasattr(builder, 'build'), "CorpusBuilder should not have build() method"


def test_project_builder_has_no_build_method():
    """Test that ProjectBuilder doesn't have build() method."""
    import kathairo

    builder = kathairo.from_usfm_corpus("path/to/corpus") \
        .with_project_name("TestProject")

    assert type(builder).__name__ == "ProjectBuilder"
    assert not hasattr(builder, 'build'), "ProjectBuilder should not have build() method"


def test_complete_builder_has_build_method():
    """Test that CompleteBuilder has build() method."""
    import kathairo

    builder = kathairo.from_usfm_corpus("path/to/corpus") \
        .with_project_name("TestProject") \
        .with_output_dir("output")

    assert type(builder).__name__ == "CompleteBuilder"
    assert hasattr(builder, 'build'), "CompleteBuilder should have build() method"


def test_complete_builder_with_language():
    """Test that CompleteBuilder is created when using with_language()."""
    import kathairo

    builder = kathairo.from_usfm_corpus("path/to/corpus") \
        .with_project_name("TestProject") \
        .with_language("eng")

    assert type(builder).__name__ == "CompleteBuilder"
    assert hasattr(builder, 'build'), "CompleteBuilder should have build() method after with_language()"


def test_config_builder_has_build_method():
    """Test that ConfigBuilder has build() method immediately."""
    import kathairo

    # from_config_file returns ConfigBuilder
    builder = kathairo.from_config_file("path/to/config.json")

    assert type(builder).__name__ == "ConfigBuilder"
    assert hasattr(builder, 'build'), "ConfigBuilder should have build() method"


def test_builder_state_progression():
    """Test the full state progression of the builder."""
    import kathairo

    # Start with CorpusBuilder
    corpus_builder = kathairo.from_usfm_corpus("path")
    assert type(corpus_builder).__name__ == "CorpusBuilder"

    # Progress to ProjectBuilder
    project_builder = corpus_builder.with_project_name("Test")
    assert type(project_builder).__name__ == "ProjectBuilder"

    # Progress to CompleteBuilder
    complete_builder = project_builder.with_output_dir("output")
    assert type(complete_builder).__name__ == "CompleteBuilder"

    # Verify only CompleteBuilder has build()
    assert not hasattr(corpus_builder, 'build')
    assert not hasattr(project_builder, 'build')
    assert hasattr(complete_builder, 'build')


def test_builder_methods_return_correct_type():
    """Test that builder methods return the correct builder type."""
    import kathairo

    # CorpusBuilder methods return CorpusBuilder
    builder = kathairo.from_usfm_corpus("path")
    assert type(builder.with_versification("vrs")).__name__ == "CorpusBuilder"
    assert type(builder.use_latin_ws_tokenizer()).__name__ == "CorpusBuilder"

    # ProjectBuilder methods return ProjectBuilder
    builder2 = builder.with_project_name("Test")
    assert type(builder2.exclude_cross_references()).__name__ == "ProjectBuilder"
    assert type(builder2.with_versification("vrs")).__name__ == "ProjectBuilder"

    # CompleteBuilder methods return CompleteBuilder
    builder3 = builder2.with_output_dir("output")
    assert type(builder3.use_chinese_tokenizer()).__name__ == "CompleteBuilder"
    assert type(builder3.exclude_bracketed_text()).__name__ == "CompleteBuilder"
