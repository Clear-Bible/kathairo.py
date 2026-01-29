from .params import Param
from .api import create_tsv


class TSVBuilder:
    def __init__(self):
        self._config = {}

    def with_versification(self, path):
        self._config[Param.VERSIFICATION_PATH] = path
        return self

    def use_latin_tokenizer(self):
        self._config[Param.USE_LATIN_TOKENIZER] = True
        return self

    def use_latin_ws_tokenizer(self):
        self._config[Param.USE_LATIN_WS_TOKENIZER] = True
        return self

    def use_chinese_tokenizer(self):
        self._config[Param.USE_CHINESE_TOKENIZER] = True
        return self

    def exclude_bracketed_text(self):
        self._config[Param.EXCLUDE_BRACKETS] = True
        return self

    def exclude_cross_references(self):
        self._config[Param.EXCLUDE_XREFS] = True
        return self

    def with_psalm_superscription_tag(self, tag):
        self._config[Param.PSALM_SUPERSCRIPTION_TAG] = tag
        return self

    def treat_apostrophe_as_single_quote(self):
        self._config[Param.APOSTROPHE_AS_QUOTE] = True
        return self

    def with_regex_rules(self, path):
        self._config[Param.REGEX_RULES_PATH] = path
        return self

    def with_stop_words(self, path):
        self._config[Param.STOP_WORDS_PATH] = path
        return self

    def with_zw_removal(self, path):
        self._config[Param.ZW_REMOVAL_PATH] = path
        return self

    def with_language(self, lang):
        self._config[Param.LANGUAGE] = lang
        return self

    def with_project_name(self, name):
        self._config[Param.PROJECT_NAME] = name
        return self

    def with_output_dir(self, path):
        self._config[Param.OUTPUT_DIR] = path
        return self

    def with_metadata_source_url(self, url):
        self._config[Param.METADATA_SOURCE_URL] = url
        return self

    def with_metadata_path(self, path):
        self._config[Param.METADATA_PATH] = path
        return self

    def with_metadata_kind(self, kind):
        self._config[Param.METADATA_KIND] = kind
        return self

    def build(self):
        if hasattr(self, '_config_path'):
            return create_tsv(config_path=self._config_path)
        elif hasattr(self, '_config_object'):
            return create_tsv(config_object=self._config_object)
        else:
            return create_tsv(config_object=self._config)


def from_usfm_corpus(path):
    builder = TSVBuilder()
    builder._config[Param.USFM_PATH] = path
    return builder


def from_usx_corpus(path):
    builder = TSVBuilder()
    builder._config[Param.USX_PATH] = path
    return builder


def from_tsv(path):
    builder = TSVBuilder()
    builder._config[Param.TSV_PATH] = path
    return builder


def from_config_file(path):
    builder = TSVBuilder()
    builder._config_path = path
    return builder


def from_config(obj):
    builder = TSVBuilder()
    builder._config_object = obj
    return builder
