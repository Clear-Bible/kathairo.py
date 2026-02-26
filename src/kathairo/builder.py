from typing import Union
from .params import Param
from .api import create_tsv


class CompleteBuilder:
    """Builder with all required fields set. Can call build()."""

    def __init__(self, config: dict):
        self._config = config

    def with_versification(self, path: str) -> 'CompleteBuilder':
        self._config[Param.VERSIFICATION_PATH] = path
        return self

    def use_latin_tokenizer(self) -> 'CompleteBuilder':
        self._config[Param.USE_LATIN_TOKENIZER] = True
        return self

    def use_latin_ws_tokenizer(self) -> 'CompleteBuilder':
        self._config[Param.USE_LATIN_WS_TOKENIZER] = True
        return self

    def use_chinese_tokenizer(self) -> 'CompleteBuilder':
        self._config[Param.USE_CHINESE_TOKENIZER] = True
        return self

    def exclude_bracketed_text(self) -> 'CompleteBuilder':
        self._config[Param.EXCLUDE_BRACKETS] = True
        return self

    def exclude_cross_references(self) -> 'CompleteBuilder':
        self._config[Param.EXCLUDE_XREFS] = True
        return self

    def with_psalm_superscription_tag(self, tag: str) -> 'CompleteBuilder':
        self._config[Param.PSALM_SUPERSCRIPTION_TAG] = tag
        return self

    def treat_apostrophe_as_single_quote(self) -> 'CompleteBuilder':
        self._config[Param.APOSTROPHE_AS_QUOTE] = True
        return self

    def with_regex_rules(self, path: str) -> 'CompleteBuilder':
        self._config[Param.REGEX_RULES_PATH] = path
        return self

    def with_stop_words(self, path: str) -> 'CompleteBuilder':
        self._config[Param.STOP_WORDS_PATH] = path
        return self

    def with_zw_removal(self, path: str) -> 'CompleteBuilder':
        self._config[Param.ZW_REMOVAL_PATH] = path
        return self

    def with_metadata_source_url(self, url: str) -> 'CompleteBuilder':
        self._config[Param.METADATA_SOURCE_URL] = url
        return self

    def with_metadata_path(self, path: str) -> 'CompleteBuilder':
        self._config[Param.METADATA_PATH] = path
        return self

    def with_metadata_kind(self, kind: str) -> 'CompleteBuilder':
        self._config[Param.METADATA_KIND] = kind
        return self

    def with_section_trees(self) -> 'CompleteBuilder':
        self._config[Param.WITH_SECTION_TREES] = True
        return self

    def build(self) -> None:
        """Build and execute TSV creation."""
        return create_tsv(config_object=self._config)


class ProjectBuilder:
    """Builder with corpus and project name set. Needs output location."""

    def __init__(self, config: dict):
        self._config = config

    def with_versification(self, path: str) -> 'ProjectBuilder':
        self._config[Param.VERSIFICATION_PATH] = path
        return self

    def use_latin_tokenizer(self) -> 'ProjectBuilder':
        self._config[Param.USE_LATIN_TOKENIZER] = True
        return self

    def use_latin_ws_tokenizer(self) -> 'ProjectBuilder':
        self._config[Param.USE_LATIN_WS_TOKENIZER] = True
        return self

    def use_chinese_tokenizer(self) -> 'ProjectBuilder':
        self._config[Param.USE_CHINESE_TOKENIZER] = True
        return self

    def exclude_bracketed_text(self) -> 'ProjectBuilder':
        self._config[Param.EXCLUDE_BRACKETS] = True
        return self

    def exclude_cross_references(self) -> 'ProjectBuilder':
        self._config[Param.EXCLUDE_XREFS] = True
        return self

    def with_psalm_superscription_tag(self, tag: str) -> 'ProjectBuilder':
        self._config[Param.PSALM_SUPERSCRIPTION_TAG] = tag
        return self

    def treat_apostrophe_as_single_quote(self) -> 'ProjectBuilder':
        self._config[Param.APOSTROPHE_AS_QUOTE] = True
        return self

    def with_regex_rules(self, path: str) -> 'ProjectBuilder':
        self._config[Param.REGEX_RULES_PATH] = path
        return self

    def with_stop_words(self, path: str) -> 'ProjectBuilder':
        self._config[Param.STOP_WORDS_PATH] = path
        return self

    def with_zw_removal(self, path: str) -> 'ProjectBuilder':
        self._config[Param.ZW_REMOVAL_PATH] = path
        return self

    def with_metadata_source_url(self, url: str) -> 'ProjectBuilder':
        self._config[Param.METADATA_SOURCE_URL] = url
        return self

    def with_metadata_path(self, path: str) -> 'ProjectBuilder':
        self._config[Param.METADATA_PATH] = path
        return self

    def with_metadata_kind(self, kind: str) -> 'ProjectBuilder':
        self._config[Param.METADATA_KIND] = kind
        return self

    def with_section_trees(self) -> 'ProjectBuilder':
        self._config[Param.WITH_SECTION_TREES] = True
        return self

    def with_output_dir(self, path: str) -> CompleteBuilder:
        """Set output directory. Returns CompleteBuilder that can build()."""
        self._config[Param.OUTPUT_DIR] = path
        return CompleteBuilder(self._config)

    def with_language(self, lang: str) -> CompleteBuilder:
        """Set language for default output path. Returns CompleteBuilder that can build()."""
        self._config[Param.LANGUAGE] = lang
        return CompleteBuilder(self._config)


class CorpusBuilder:
    """Builder with corpus set. Needs project name."""

    def __init__(self, config: dict):
        self._config = config

    def with_versification(self, path: str) -> 'CorpusBuilder':
        self._config[Param.VERSIFICATION_PATH] = path
        return self

    def use_latin_tokenizer(self) -> 'CorpusBuilder':
        self._config[Param.USE_LATIN_TOKENIZER] = True
        return self

    def use_latin_ws_tokenizer(self) -> 'CorpusBuilder':
        self._config[Param.USE_LATIN_WS_TOKENIZER] = True
        return self

    def use_chinese_tokenizer(self) -> 'CorpusBuilder':
        self._config[Param.USE_CHINESE_TOKENIZER] = True
        return self

    def exclude_bracketed_text(self) -> 'CorpusBuilder':
        self._config[Param.EXCLUDE_BRACKETS] = True
        return self

    def exclude_cross_references(self) -> 'CorpusBuilder':
        self._config[Param.EXCLUDE_XREFS] = True
        return self

    def with_psalm_superscription_tag(self, tag: str) -> 'CorpusBuilder':
        self._config[Param.PSALM_SUPERSCRIPTION_TAG] = tag
        return self

    def treat_apostrophe_as_single_quote(self) -> 'CorpusBuilder':
        self._config[Param.APOSTROPHE_AS_QUOTE] = True
        return self

    def with_regex_rules(self, path: str) -> 'CorpusBuilder':
        self._config[Param.REGEX_RULES_PATH] = path
        return self

    def with_stop_words(self, path: str) -> 'CorpusBuilder':
        self._config[Param.STOP_WORDS_PATH] = path
        return self

    def with_zw_removal(self, path: str) -> 'CorpusBuilder':
        self._config[Param.ZW_REMOVAL_PATH] = path
        return self

    def with_metadata_source_url(self, url: str) -> 'CorpusBuilder':
        self._config[Param.METADATA_SOURCE_URL] = url
        return self

    def with_metadata_path(self, path: str) -> 'CorpusBuilder':
        self._config[Param.METADATA_PATH] = path
        return self

    def with_metadata_kind(self, kind: str) -> 'CorpusBuilder':
        self._config[Param.METADATA_KIND] = kind
        return self

    def with_section_trees(self) -> 'CorpusBuilder':
        self._config[Param.WITH_SECTION_TREES] = True
        return self

    def with_project_name(self, name: str) -> ProjectBuilder:
        """Set project name. Returns ProjectBuilder that needs output location."""
        self._config[Param.PROJECT_NAME] = name
        return ProjectBuilder(self._config)


class ConfigBuilder:
    """Builder for config file/object. Already complete, can build directly."""

    def __init__(self, config_path: str = None, config_object: dict = None):
        self._config_path = config_path
        self._config_object = config_object

    def build(self) -> None:
        """Build and execute TSV creation."""
        if self._config_path:
            return create_tsv(config_path=self._config_path)
        else:
            return create_tsv(config_object=self._config_object)


def from_usfm_corpus(path: str) -> CorpusBuilder:
    """Start building from USFM corpus. Next: set project name with .with_project_name()"""
    config = {Param.USFM_PATH: path}
    return CorpusBuilder(config)


def from_usx_corpus(path: str) -> CorpusBuilder:
    """Start building from USX corpus. Next: set project name with .with_project_name()"""
    config = {Param.USX_PATH: path}
    return CorpusBuilder(config)


def from_tsv(path: str) -> CorpusBuilder:
    """Start building from TSV file. Next: set project name with .with_project_name()"""
    config = {Param.TSV_PATH: path}
    return CorpusBuilder(config)


def from_config_file(path: str) -> ConfigBuilder:
    """Build from config file. Can call .build() immediately."""
    return ConfigBuilder(config_path=path)


def from_config(obj: dict) -> ConfigBuilder:
    """Build from config object. Can call .build() immediately."""
    return ConfigBuilder(config_object=obj)
