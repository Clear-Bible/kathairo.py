class Param:
    JSON_PATH = "json_path"
    CONFIG = "config"

    USFM_PATH = "targetUsfmCorpusPath"
    USX_PATH = "targetUsxCorpusPath"
    TSV_PATH = "tsvPath"

    VERSIFICATION_PATH = "targetVersificationPath"

    USE_LATIN_TOKENIZER = "latinTokenizer"
    USE_LATIN_WS_TOKENIZER = "latinWhiteSpaceIncludedTokenizer"
    USE_CHINESE_TOKENIZER = "chineseTokenizer"

    EXCLUDE_BRACKETS = "excludeBracketedText"
    EXCLUDE_XREFS = "excludeCrossReferences"
    PSALM_SUPERSCRIPTION_TAG = "psalmSuperscriptionTag"
    APOSTROPHE_AS_QUOTE = "treatApostropheAsSingleQuote"
    REGEX_RULES_PATH = "regexRulesPath"
    STOP_WORDS_PATH = "stopWordsPath"
    ZW_REMOVAL_PATH = "zwRemovalPath"

    LANGUAGE = "language"
    PROJECT_NAME = "projectName"
    OUTPUT_DIR = "output_dir"

    METADATA_SOURCE_URL = "metadata_source_url"
    METADATA_PATH = "metadata_path"
    METADATA_KIND = "metadata_kind"


class ParamGroups:
    CORPUS_INPUTS = [
        Param.USFM_PATH,
        Param.USX_PATH,
        Param.TSV_PATH,
    ]

    TOKENIZERS = [
        Param.USE_LATIN_TOKENIZER,
        Param.USE_LATIN_WS_TOKENIZER,
        Param.USE_CHINESE_TOKENIZER,
    ]

    OUTPUT_NAMING = [
        Param.PROJECT_NAME,
        Param.LANGUAGE,
        Param.OUTPUT_DIR,
    ]

    BOOLEAN_FLAGS = [
        Param.EXCLUDE_BRACKETS,
        Param.EXCLUDE_XREFS,
        Param.APOSTROPHE_AS_QUOTE,
        Param.USE_LATIN_TOKENIZER,
        Param.USE_LATIN_WS_TOKENIZER,
        Param.USE_CHINESE_TOKENIZER,
    ]
