from .params import ParamHelper, ParamGroups
from .tsvs import build_tsv_json_parser
import json


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
    output_dir=None,

    metadata_source_url=None,
    metadata_path=None,
    metadata_kind=None
):

    config_list = _normalize_to_config_list(
        config_path=config_path,
        config_object=config_object,
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
        output_dir=output_dir,
        metadata_source_url=metadata_source_url,
        metadata_path=metadata_path,
        metadata_kind=metadata_kind
    )

    for config_dict in config_list:
        _validate_config(config_dict)

    build_tsv_json_parser.main(config_list)

def get_config_list_from_file(config_path):
    with open(config_path) as file:
        config_list = json.load(file)

    solo_project = next((config_dict for config_dict in config_list if "solo" in config_dict), None)
    if(solo_project is not None):
        config_list = [solo_project]

    return config_list

def _normalize_to_config_list(config_path, config_object, **params):

    if config_path is not None:
        return get_config_list_from_file(config_path)

    if config_object is not None:
        if isinstance(config_object, list):
            return config_object
        else:
            return [config_object]

    config_dict = {k: v for k, v in params.items() if v is not None}
    return [config_dict]


def _validate_config(config_dict):

    corpus_inputs = [
        ParamHelper.get_python_name(p) for p in ParamGroups.CORPUS_INPUTS
    ]
    provided_corpus = [k for k in corpus_inputs if k in config_dict and config_dict[k]]

    if len(provided_corpus) == 0:
        raise ValueError(
            f"Must provide exactly one corpus input: {', '.join(corpus_inputs)}"
        )
    if len(provided_corpus) > 1:
        raise ValueError(
            f"Cannot provide multiple corpus inputs. Got: {', '.join(provided_corpus)}"
        )

    has_output_dir = config_dict.get('output_dir')
    has_project_name = config_dict.get('projectName')
    has_language = config_dict.get('language')

    if not has_project_name:
        raise ValueError("Must provide 'projectName'")

    if not has_output_dir and not has_language:
        raise ValueError("Must provide either 'output_dir' or 'language'")

    tokenizers = [
        ParamHelper.get_python_name(p) for p in ParamGroups.TOKENIZERS
    ]
    provided_tokenizers = [k for k in tokenizers if config_dict.get(k) is True]

    if len(provided_tokenizers) > 1:
        raise ValueError(
            f"Cannot specify multiple tokenizers. Got: {', '.join(provided_tokenizers)}"
        )
