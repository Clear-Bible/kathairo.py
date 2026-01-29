from .params import ParamHelper, ParamGroups
from .tsvs import build_tsv_json_parser


def create_tsv(
    config_path=None,
    config_object=None,

    targetUsfmCorpusPath=None,
    targetUsxCorpusPath=None,
    tsvPath=None,

    targetVersificationPath=None,

    latinWhiteSpaceIncludedTokenizer=False,
    chineseTokenizer=False,

    excludeBracketedText=False,
    excludeCrossReferences=False,
    psalmSuperscriptionTag='d',
    treatApostropheAsSingleQuote=False,
    regexRulesPath=None,
    stopWordsPath=None,
    zwRemovalPath=None,

    language=None,
    projectName=None,
    output_path=None,

    metadata_source_url=None,
    metadata_path=None,
    metadata_kind=None
):
    if config_path is not None:
        _process_from_file(config_path)
        return

    if config_object is not None:
        _process_from_object(config_object)
        return

    config_dict = _build_config_from_params(
        targetUsfmCorpusPath=targetUsfmCorpusPath,
        targetUsxCorpusPath=targetUsxCorpusPath,
        tsvPath=tsvPath,
        targetVersificationPath=targetVersificationPath,
        latinWhiteSpaceIncludedTokenizer=latinWhiteSpaceIncludedTokenizer,
        chineseTokenizer=chineseTokenizer,
        excludeBracketedText=excludeBracketedText,
        excludeCrossReferences=excludeCrossReferences,
        psalmSuperscriptionTag=psalmSuperscriptionTag,
        treatApostropheAsSingleQuote=treatApostropheAsSingleQuote,
        regexRulesPath=regexRulesPath,
        stopWordsPath=stopWordsPath,
        zwRemovalPath=zwRemovalPath,
        language=language,
        projectName=projectName,
        output_path=output_path,
        metadata_source_url=metadata_source_url,
        metadata_path=metadata_path,
        metadata_kind=metadata_kind
    )

    _process_from_object(config_dict)


def _process_from_file(json_path):
    build_tsv_json_parser.main(json_path)


def _process_from_object(config):
    _validate_config(config)
    build_tsv_json_parser.process_corpus(config)


def _build_config_from_params(**kwargs):
    config = {k: v for k, v in kwargs.items() if v is not None}
    _validate_config(config)
    return config


def _validate_config(config):
    corpus_inputs = [
        ParamHelper.get_python_name(p) for p in ParamGroups.CORPUS_INPUTS
    ]
    provided_corpus = [k for k in corpus_inputs if k in config and config[k]]

    if len(provided_corpus) == 0:
        raise ValueError(
            f"Must provide exactly one corpus input: {', '.join(corpus_inputs)}"
        )
    if len(provided_corpus) > 1:
        raise ValueError(
            f"Cannot provide multiple corpus inputs. Got: {', '.join(provided_corpus)}"
        )

    has_output_path = config.get('output_path')
    has_project_name = config.get('projectName')
    has_language = config.get('language')

    if not has_output_path:
        if not has_project_name:
            raise ValueError("Must provide 'projectName' when not using 'output_path'")
        if not has_language:
            raise ValueError("Must provide 'language' when not using 'output_path'")

    tokenizers = [
        ParamHelper.get_python_name(p) for p in ParamGroups.TOKENIZERS
    ]
    provided_tokenizers = [k for k in tokenizers if config.get(k) is True]

    if len(provided_tokenizers) > 1:
        raise ValueError(
            f"Cannot specify multiple tokenizers. Got: {', '.join(provided_tokenizers)}"
        )
