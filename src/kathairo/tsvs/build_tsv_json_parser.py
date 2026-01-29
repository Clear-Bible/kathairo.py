import time
start = time.time()

from concurrent.futures import ProcessPoolExecutor, as_completed

from kathairo.tokenization.ChineseBibleWordTokenizer import ChineseBibleWordTokenizer
from machine.tokenization import LatinWordTokenizer
from kathairo.tokenization.latin_whitespace_included_tokenizer import LatinWhitespaceIncludedWordTokenizer
from kathairo.tokenization.regex_rules import DefaultRegexRules

from kathairo.parsing.usx.usx_file_text_corpus import UsxFileTextCorpus
from kathairo.parsing.usfm.usfm_file_text_corpus import UsfmFileTextCorpus
from kathairo.parsing.usfm.usfm_handlers import ModifiedTextRowCollector

from machine.scripture import ORIGINAL_VERSIFICATION, Versification
from kathairo.helpers.paths import import_module_from_path

from kathairo.tsvs.build_tsv import corpus_to_tsv, tokens_to_tsv

import pandas as pd

SOURCE_VERSIFICATION = Versification(name="sourceVersification", base_versification=ORIGINAL_VERSIFICATION)

def create_tokenizer(config_dict, regex_rules_class):
    treat_apostrophe_as_single_quote = config_dict.get("treatApostropheAsSingleQuote", False)
    language = config_dict.get("language")

    if config_dict.get("chineseTokenizer"):
        return ChineseBibleWordTokenizer()
    elif config_dict.get("latinTokenizer"):
        return LatinWordTokenizer(treat_apostrophe_as_single_quote=treat_apostrophe_as_single_quote)
    elif config_dict.get("latinWhiteSpaceIncludedTokenizer"):
        return LatinWhitespaceIncludedWordTokenizer(
            treat_apostrophe_as_single_quote=treat_apostrophe_as_single_quote,
            language=language,
            regex_rules_class=regex_rules_class
        )
    return None

def create_corpus(config_dict, target_versification, psalm_superscription_tag):
    if "targetUsfmCorpusPath" in config_dict:
        return UsfmFileTextCorpus(
                config_dict["targetUsfmCorpusPath"],
            handler=ModifiedTextRowCollector,
            versification=target_versification,
            psalmSuperscriptionTag=psalm_superscription_tag
        )
    return UsxFileTextCorpus(
        config_dict["targetUsxCorpusPath"],
        versification=target_versification
    )

def get_config(config_dict):
    processed_config = {}

    regex_rules_class = DefaultRegexRules()
    if "regexRulesPath" in config_dict:
        regex_rules_module = import_module_from_path("regex_rules", config_dict["regexRulesPath"])
        regex_rules_class = getattr(regex_rules_module, "CustomRegexRules", DefaultRegexRules)()
    processed_config["regexRulesClass"] = regex_rules_class

    processed_config["tokenizer"] = create_tokenizer(config_dict, regex_rules_class)

    target_versification_path = config_dict.get("targetVersificationPath")
    processed_config["targetVersificationPath"] = target_versification_path
    processed_config["targetVersification"] = Versification.load(target_versification_path, fallback_name="web")

    processed_config["psalmSuperscriptionTag"] = config_dict.get("psalmSuperscriptionTag", 'd')

    processed_config["projectName"] = config_dict.get("projectName")
    if "tsvPath" in config_dict:
        processed_config["tsvPath"] = config_dict.get("tsvPath")
        processed_config["isCorpus"] = False
    else:
        processed_config["corpus"] = create_corpus(config_dict, processed_config["targetVersification"], processed_config["psalmSuperscriptionTag"])
        processed_config["isCorpus"] = True

    processed_config["excludeBracketedText"] = config_dict.get("excludeBracketedText", False)
    processed_config["excludeCrossReferences"] = config_dict.get("excludeCrossReferences", False)
    processed_config["language"] = config_dict.get("language")

    zw_removal_path = config_dict.get("zwRemovalPath")
    processed_config["zwRemovalDf"] = pd.read_csv(zw_removal_path, sep='\t', dtype=str) if zw_removal_path else None

    stop_words_path = config_dict.get("stopWordsPath")
    processed_config["stopWordsDf"] = pd.read_csv(stop_words_path, sep='\t', dtype=str) if stop_words_path else None

    return processed_config

def process_corpus(config_dict):

    processed_config = get_config(config_dict)

    if(processed_config["isCorpus"]):
        return{
            'corpus_to_tsv': corpus_to_tsv(
                targetVersification=processed_config["targetVersification"],
                sourceVersification=SOURCE_VERSIFICATION,
                corpus=processed_config["corpus"],
                tokenizer=processed_config["tokenizer"],
                project_name=processed_config["projectName"],
                excludeBracketedText=processed_config["excludeBracketedText"],
                excludeCrossReferences=processed_config["excludeCrossReferences"],
                language=processed_config["language"],
                zwRemovalDf=processed_config["zwRemovalDf"],
                stopWordsDf=processed_config["stopWordsDf"],
                regex_rules_class=processed_config["regexRulesClass"]
            )
        }
    else:
        return{
            'tokens_to_tsv': tokens_to_tsv(
                targetVersification=processed_config["targetVersification"],
                sourceVersification=SOURCE_VERSIFICATION,
                tsvPath=processed_config["tsvPath"],
                project_name=processed_config["projectName"],
                language=processed_config["language"],
                zwRemovalDf=processed_config["zwRemovalDf"],
                stopWordsDf=processed_config["stopWordsDf"],
                excludeBracketedText=processed_config["excludeBracketedText"],
                excludeCrossReferences=processed_config["excludeCrossReferences"],
                regex_rules_class=processed_config["regexRulesClass"]
            )
        }

def main(config_list):

    with ProcessPoolExecutor() as executor:

        futures = {executor.submit(process_corpus, config_dict): config_dict for config_dict in config_list}

        for future in as_completed(futures):
            try:
                result = future.result()
                print(f"Elapsed time: {time.time() - start:.2f} seconds")
            except Exception as e:
                config_dict = futures[future]
                project_name = config_dict.get('projectName', 'Unknown')
                print(f"Task for {project_name} generated an exception: {e}")

    print(f"Total elapsed time: {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    main()
