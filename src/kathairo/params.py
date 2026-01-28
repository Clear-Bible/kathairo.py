class Param:
    JSON_PATH = ("json", "json_path")
    CONFIG = ("config", "config")

    USFM_CORPUS_PATH = ("usfm", "targetUsfmCorpusPath")
    USX_CORPUS_PATH = ("usx", "targetUsxCorpusPath")
    TSV_PATH = ("tsv", "tsvPath")

    VERSIFICATION_PATH = ("vrs", "targetVersificationPath")

    USE_LATIN_TOKENIZER = ("latin-ws", "latinWhiteSpaceIncludedTokenizer")
    USE_CHINESE_TOKENIZER = ("chinese", "chineseTokenizer")

    EXCLUDE_BRACKETS = ("no-brackets", "excludeBracketedText")
    EXCLUDE_XREFS = ("no-xrefs", "excludeCrossReferences")
    PSALM_SUPERSCRIPTION_TAG = ("super-tag", "psalmSuperscriptionTag")
    APOSTROPHE_AS_QUOTE = ("apostrophe-quote", "treatApostropheAsSingleQuote")
    REGEX_RULES_PATH = ("regex", "regexRulesPath")
    STOP_WORDS_PATH = ("stop-words", "stopWordsPath")
    ZW_REMOVAL_PATH = ("zw-removal", "zwRemovalPath")

    LANGUAGE = ("lang", "language")
    PROJECT_NAME = ("project", "projectName")
    OUTPUT_PATH = ("output", "output_path")

    METADATA_SOURCE_URL = ("source-url", "metadata_source_url")
    METADATA_PATH = ("meta-path", "metadata_path")
    METADATA_KIND = ("meta-kind", "metadata_kind")


class ParamHelper:

    @staticmethod
    def get_cli_name(param_tuple):
        return param_tuple[0]

    @staticmethod
    def get_python_name(param_tuple):
        return param_tuple[1]

    @staticmethod
    def all_params():
        return [
            getattr(Param, attr) for attr in dir(Param)
            if not attr.startswith('_') and isinstance(getattr(Param, attr), tuple)
        ]

    @staticmethod
    def cli_to_python_map():
        return {
            param[0]: param[1] for param in ParamHelper.all_params()
        }

    @staticmethod
    def python_to_cli_map():
        return {
            param[1]: param[0] for param in ParamHelper.all_params()
        }


class ParamGroups:
    CORPUS_INPUTS = [
        Param.USFM_CORPUS_PATH,
        Param.USX_CORPUS_PATH,
        Param.TSV_PATH,
    ]

    TOKENIZERS = [
        Param.USE_LATIN_TOKENIZER,
        Param.USE_CHINESE_TOKENIZER,
    ]

    OUTPUT_NAMING = [
        Param.PROJECT_NAME,
        Param.LANGUAGE,
        Param.OUTPUT_PATH,
    ]

    BOOLEAN_FLAGS = [
        Param.EXCLUDE_BRACKETS,
        Param.EXCLUDE_XREFS,
        Param.APOSTROPHE_AS_QUOTE,
        Param.USE_LATIN_TOKENIZER,
        Param.USE_CHINESE_TOKENIZER,
    ]
